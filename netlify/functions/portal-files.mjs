// Portál 12 Weeks Race Prep: seznam a stažení PDF jen pro přihlášené účastníky.
// Registrace v Netlify Identity je jen na pozvánku, takže každý přihlášený uživatel je účastník.
import { getUser } from "@netlify/identity";
import { readFile } from "node:fs/promises";
import path from "node:path";

const BASES = [
  path.join(process.cwd(), "portal-files"),
  path.join(path.dirname(new URL(import.meta.url).pathname), "..", "..", "portal-files"),
];

async function read(rel) {
  for (const base of BASES) {
    try { return await readFile(path.join(base, rel)); } catch {}
  }
  return null;
}

export default async (req) => {
  const user = await getUser();
  if (!user) return Response.json({ error: "unauthorized" }, { status: 401, headers: { "cache-control": "no-store" } });

  const raw = await read("manifest.json");
  if (!raw) return Response.json({ error: "manifest missing" }, { status: 500 });
  const manifest = JSON.parse(raw.toString());

  const id = new URL(req.url).searchParams.get("f");
  if (!id) {
    const files = manifest.files.map(({ id, no, name, desc, available, note, versions, i18n }) => ({ id, no, name, desc, available, note, i18n, langs: available ? Object.keys(versions || {}) : [] }));
    return Response.json({ user: { email: user.email, name: user.name || "" }, files }, { headers: { "cache-control": "no-store" } });
  }

  const lang = new URL(req.url).searchParams.get("lang") || "cs";
  const item = /^[a-z0-9-]+$/.test(id) && manifest.files.find((f) => f.id === id && f.available);
  const file = item && item.versions && (item.versions[lang] || item.versions.cs);
  const buf = file && (await read(path.basename(file)));
  if (!buf) return new Response("Soubor není k dispozici.", { status: 404 });
  return new Response(buf, {
    headers: {
      "content-type": "application/pdf",
      "content-disposition": `attachment; filename="${path.basename(file)}"`,
      "cache-control": "private, no-store",
    },
  });
};

export const config = { path: "/api/portal-files" };
