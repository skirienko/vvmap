#!/usr/bin/env python3
"""Download Vladivostok OSM data, trying Overpass mirrors in order."""

from __future__ import annotations

import argparse
import os
import ssl
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import certifi


OVERPASS_SERVERS = [
    "https://overpass.kumi.systems/api/",
    "https://z.overpass-api.de/api/",
    "https://maps.mail.ru/osm/tools/overpass/api/",
    "https://overpass.osm.rambler.ru/cgi/",
    "https://overpass.private.coffee/api/",
    "https://overpass-api.de/api/",  # last resort
]

DEFAULT_OUTPUT = Path("vladivostok.osm")
DEFAULT_QUERY = Path("vladivostok.overpassql")
DEFAULT_MIN_BYTES = 100_000
DEFAULT_TIMEOUT = 90
CHUNK_SIZE = 1024 * 1024
TLS_CONTEXT = ssl.create_default_context(cafile=certifi.where())


def endpoint(server: str) -> str:
    return f"{server.rstrip('/')}/interpreter"


def download_to_temp(
    url: str,
    query: bytes,
    output_dir: Path,
    timeout: int,
) -> Path:
    request = urllib.request.Request(
        url,
        data=query,
        method="POST",
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "Referer": "https://vvmap.netlify.app/",
            "User-Agent": "vvmap-map-downloader/1.0",
        },
    )
    response = urllib.request.urlopen(request, timeout=timeout, context=TLS_CONTEXT)
    temp = tempfile.NamedTemporaryFile(
        mode="wb", prefix=".vladivostok.osm.", suffix=".tmp", dir=output_dir, delete=False
    )
    temp_path = Path(temp.name)
    try:
        with response, temp:
            shutil.copyfileobj(response, temp, length=CHUNK_SIZE)
        return temp_path
    except Exception:
        temp.close()
        temp_path.unlink(missing_ok=True)
        raise


def validate_osm(path: Path, minimum_bytes: int) -> tuple[bool, str]:
    size = path.stat().st_size
    if size < minimum_bytes:
        return False, f"response is only {size:,} bytes (minimum {minimum_bytes:,})"

    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return False, f"invalid XML ({exc})"

    if root.tag.rsplit("}", 1)[-1] != "osm":
        return False, f"root element is <{root.tag}>, not <osm>"

    element_count = sum(1 for child in root if child.tag.rsplit("}", 1)[-1] in {"node", "way", "relation"})
    if element_count == 0:
        return False, "OSM document contains no nodes, ways, or relations"

    return True, f"valid OSM XML with {element_count:,} top-level elements ({size:,} bytes)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="destination OSM file")
    parser.add_argument("--query", type=Path, default=DEFAULT_QUERY, help="Overpass query file")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="timeout per mirror in seconds")
    parser.add_argument(
        "--min-bytes",
        type=int,
        default=DEFAULT_MIN_BYTES,
        help=f"minimum accepted response size (default: {DEFAULT_MIN_BYTES:,})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.timeout <= 0 or args.min_bytes < 0:
        print("timeout must be positive and min-bytes cannot be negative", file=sys.stderr)
        return 2
    if not args.query.is_file():
        print(f"query file not found: {args.query}", file=sys.stderr)
        return 2

    query = args.query.read_bytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    for number, server in enumerate(OVERPASS_SERVERS, start=1):
        url = endpoint(server)
        temp_path: Path | None = None
        print(f"[{number}/{len(OVERPASS_SERVERS)}] trying {url}")
        try:
            temp_path = download_to_temp(url, query, args.output.parent, args.timeout)
            valid, reason = validate_osm(temp_path, args.min_bytes)
            if not valid:
                print(f"  rejected: {reason}")
                continue
            os.replace(temp_path, args.output)
            print(f"  saved {args.output}: {reason}")
            return 0
        except urllib.error.HTTPError as exc:
            print(f"  rejected: HTTP {exc.code} {exc.reason}")
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, ssl.SSLCertVerificationError):
                print(f"  failed: TLS certificate verification ({exc.reason})")
            else:
                print(f"  failed: {exc}")
        except (TimeoutError, OSError) as exc:
            print(f"  failed: {exc}")
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    print("all Overpass mirrors failed; existing output was left unchanged", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
