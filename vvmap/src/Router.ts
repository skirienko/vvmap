export interface Route {
  path: string;
  description: string;
  callback: () => void;
}

export default class Router {
  routes: Route[];
  currentRoute: Route;
  
  constructor(routes: Route[]) {
    this.routes = routes;
    this.currentRoute = routes[0];
    this._loadInitialRoute();
  }

  _loadInitialRoute() {
    const path = window.location.pathname;
    this.loadRoute(path);
  }

  _matchUrlToRoute(path: string) {
    return this.routes.find(route => route.path === path);
  }

  loadRoute(path: string) {
    const matchedRoute = this._matchUrlToRoute(path);
    if (matchedRoute) {
      this.currentRoute = matchedRoute;
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

  getCurrentRoute(): Route {
    return this.currentRoute;
  }
}