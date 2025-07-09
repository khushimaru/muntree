export const prerender = false;
import type { APIRoute } from "astro";

const ALLOWED_ROUTES = [
  "admin/login",
  "admin/links",
  "admin/links/",
  "links"
];

function isAllowedRoute(path: string): boolean {
  return ALLOWED_ROUTES.some((allowed) =>
    allowed.endsWith("/")
      ? path.startsWith(allowed)
      : path === allowed || path.startsWith(allowed + "/")
  );
}

const BACKEND_BASE_URL = import.meta.env.PUBLIC_ASTRO_BACKEND_URL;

export const ALL: APIRoute = async ({ request, params, url }) => {
  const pathArray = params?.path;
  const path = Array.isArray(pathArray) ? pathArray.join("/") : pathArray || "";

  if (!isAllowedRoute(path)) {
    return new Response(JSON.stringify({ error: "Forbidden path" }), {
      status: 403,
    });
  }

  const targetUrl = `${BACKEND_BASE_URL}/${path}${url.search ? "?" + url.searchParams.toString() : ""}`;

  const proxyRes = await fetch(targetUrl, {
    method: request.method,
    headers: {
      ...Object.fromEntries(request.headers),
      host: new URL(BACKEND_BASE_URL).host,
    },
    body: ["GET", "HEAD"].includes(request.method || "") ? undefined : await request.arrayBuffer(),
  });

  const resHeaders = new Headers(proxyRes.headers);
  resHeaders.delete("content-encoding");

  return new Response(proxyRes.body, {
    status: proxyRes.status,
    headers: resHeaders,
  });
};
