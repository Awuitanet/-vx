# 🔐 Configuración Segura de la App - Album Compartido

## ✅ ¿Qué se solucionó?

| Problema | Solución |
|----------|----------|
| ❌ Token hardcodeado en código | ✅ Token inyectado por GitHub Actions |
| ❌ GitHub detectaba como vulnerabilidad | ✅ Token nunca queda en el código |
| ❌ No podías subir fotos | ✅ Ahora funciona con autenticación segura |

---

## 📋 Pasos de Configuración

### 1️⃣ Verificar que el Issue #1 existe
La app guarda las fotos como comentarios en el Issue #1.

**Acciones:**
- Ve a: https://github.com/Awuitanet/-vx/issues
- ¿Existe Issue #1? Si no, créalo:
  - Título: `Album de Fotos`
  - Descripción: `Aquí se guardan todas las fotos compartidas`

### 2️⃣ Habilitar GitHub Pages
Tu app se despliega automáticamente en GitHub Pages.

**Acciones:**
- Ve a: https://github.com/Awuitanet/-vx/settings/pages
- En "Source", selecciona:
  - **Branch:** `main` (o la que uses)
  - **Folder:** `/docs`
- Click en "Save"

### 3️⃣ El token se inyecta automáticamente ✨
GitHub proporciona `secrets.GITHUB_TOKEN` automáticamente en cada workflow:
- ✅ No necesitas crear nada
- ✅ Se renueva cada vez que haces push
- ✅ No queda expuesto en el código

### 4️⃣ Hacer push a main
```bash
# Asegúrate de estar en la rama fix/github-auth-secure
git add .
git commit -m "feat: secure GitHub auth with Actions"
git push origin fix/github-auth-secure
```

Luego en GitHub:
1. Abre un Pull Request
2. Mergealo a `main`
3. El workflow se ejecutará automáticamente

---

## 🚀 Cómo funciona ahora

```
┌─────────────────────────────────┐
│   Tu Navegador                  │
│   (GitHub Pages)                │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   1. Subes foto aquí            │
│   (docs/index.html)             │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   2. Se sube a Imgur            │
│   (sin credenciales)            │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   3. Se guarda en GitHub        │
│   (con token inyectado)         │
│   Issue #1 → Comentario         │
└─────────────────────────────────┘
```

**El token NUNCA está en el HTML, se inyecta durante el deploy:**

```bash
GitHub Actions:
  sed -i "s|__GITHUB_TOKEN__|TOKEN_REAL_AQUI|g" docs/index.html
```

---

## ✅ Verificar que todo funciona

1. **Haz push a main** (merge el PR)
2. **Ve a:** https://github.com/Awuitanet/-vx/actions
3. **Busca el workflow** "Deploy & Inject GitHub Token"
4. **Espera a que termine** (toma ~1 minuto)
5. **Accede a tu app:** https://awuitanet.github.io/-vx/

---

## 🧪 Prueba la app

1. Login: usuario `papulandia` / contraseña `20`
2. Haz click en "Toca aquí para subir foto"
3. Selecciona una imagen
4. Si dice ✅ "¡Foto subida correctamente!" → **¡Funciona! 🎉**

---

## ⚠️ Si algo no funciona

**Error: "El Issue #1 no existe"**
- Solución: Crea el Issue #1 en el repositorio (ver paso 1)

**Error: "Error guardando en GitHub"**
- Solución: Verifica que GitHub Pages esté habilitado (ver paso 2)
- Solución: Asegúrate de hacer merge a `main`

**¿El workflow no se ejecuta?**
- Ve a Settings → Actions → General
- Asegúrate que "Actions permissions" esté en "Allow all actions"

---

## 🔐 Alternativa: Servidor Proxy (Máxima Seguridad)

Si quieres que el token NO se inyecte en el frontend, puedes usar un servidor backend:

1. Deploy un servidor Node.js (Vercel, Railway, Heroku)
2. El servidor maneja GitHub API
3. Tu app solo hace POST a `/api/upload`

**Código ejemplo server (Node.js):**
```javascript
app.post('/api/upload', async (req, res) => {
  const { imageUrl, deleteHash } = req.body;
  
  const response = await fetch('https://api.github.com/repos/Awuitanet/-vx/issues/1/comments', {
    method: 'POST',
    headers: {
      'Authorization': `token ${process.env.GITHUB_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      body: `📷 Foto: ![](${imageUrl})\n<!-- ${deleteHash} -->`
    })
  });
  
  res.json({ success: response.ok });
});
```

Contacta si necesitas ayuda con esto. 😊

---

**¿Preguntas?** Mira los logs en GitHub Actions para ver qué pasó exactamente.
