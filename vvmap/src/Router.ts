export interface Route {
  path: string;
  callback: () => void;
}

export default class Router {
  routes: Route[];
  
  constructor(routes: Route[]) {
    this.routes = routes;
    this._loadInitialRoute();
  }

  _loadInitialRoute() {
    const path = window.location.pathname;
    this.loadRoute(path);
  }

  _matchUrlToRoute(path: string) {
    const matchedRoute = this.routes.find(route => route.path === path);
    return matchedRoute;
  }

  loadRoute(path: string) {
    const matchedRoute = this._matchUrlToRoute(path);
    if (matchedRoute) {
      matchedRoute.callback();
    }
    else {
      this.navigateTo(this.routes[0].path);
    }
  }

  navigateTo(path: string) {
    window.history.pushState({}, '', path);
    this.loadRoute(path);
  }

}