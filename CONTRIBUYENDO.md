# Contribuyendo a Trammel PE

¡Gracias por tu interés en contribuir! Trammel PE es una herramienta comunitaria — simple, local y útil para cualquiera que trabaje con LLMs y agentes de IA.

## 🌎 Idiomas / Languages

- [English](CONTRIBUTING.md)
- [Español](CONTRIBUYENDO.md) (estás aquí)

---

## Niveles de Contribuidor

Valoramos las contribuciones de calidad de profesionales con diversos antecedentes — ingeniería, física, biología, matemáticas, lingüística y más. Para mantener la calidad del código, usamos un sistema de niveles:

### 🌱 Propuesto (Nuevos Contribuidores)

Todos los contribuidores nuevos empiezan aquí. Tus primeras contribuciones serán revisadas manualmente.

- **Cómo unirse:** Abre un issue presentándote, o envía tu primer PR
- **PRs:** Requieren aprobación manual de un Mantenedor antes de merge
- **Antecedentes:** Te animamos a compartir tu formación profesional (ingeniería, ciencia, etc.) en tu primer issue — esto nos ayuda a asignarte tareas que se ajusten a tu experiencia
- **Alcance:** Correcciones de bugs, traducciones, mejoras de documentación, adición de templates

### 🌿 Contribuidor

Después de 2+ PRs mergeados y calidad consistente, avanzas a Contribuidor.

- **PRs:** Requieren 1 aprobación de Mantenedor
- **Alcance:** Adición de features, soporte de nuevos idiomas, mejoras de UI
- **Cómo avanzar:** Calidad consistente, buena comunicación, comprensión de la arquitectura del proyecto

### 🌳 Mantenedor

Contribuidores de confianza con conocimiento profundo del proyecto. Actualmente miembros del equipo de JJ Solutions.

- **PRs:** Pueden aprobar PRs de otros contribuidores
- **Alcance:** Decisiones de arquitectura, cambios breaking, gestión de releases
- **Cómo avanzar:** Nominado por Mantenedores existentes después de contribución sostenida

## Cómo Contribuir

### Inicio Rápido

1. **Haz Fork** de este repositorio
2. **Crea** una rama: `git checkout -b mi-feature`
3. **Haz** tus cambios
4. **Prueba** abriendo `index.html` en un navegador
5. **Commit** con un mensaje claro (ver Estilo de Commits abajo)
6. **Push** y abre un Pull Request

### Estilo de Commits

Usa commits convencionales:

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `i18n:` Traducciones/internacionalización
- `style:` Cambios visuales/UI
- `refactor:` Refactorización de código
- `test:` Adición de pruebas

### Agregar un Idioma

El sistema i18n usa un objeto clave-valor en `index.html` (el objeto `I18N`). Para agregar un nuevo idioma:

1. Copia el objeto `en` dentro de `I18N`
2. Cambia la clave al código de tu idioma (ej: `fr`, `de`, `ja`, `zh`)
3. Traduce todos los valores
4. Agrega una `<option>` al dropdown `#langSelect` en el HTML
5. Prueba exhaustivamente — todas las secciones, placeholders y prompts generados deben funcionar
6. Actualiza `README.md` y `CONTRIBUYENDO.md` con la info del nuevo idioma

### Agregar un Template

Los templates se definen en la función `loadTemplate()`. Para agregar uno:

1. Agrega una nueva entrada al objeto `templates`
2. Provee traducciones para `en`, `es`, y cualquier otro idioma disponible (mínimo `en` y `es`)
3. Asegúrate de que todos los campos estén completos (objetivo, alcance, herramientas, subtareas, etc.)
4. Prueba en todos los idiomas disponibles

### Reportar Issues

- Abre un issue en [Codeberg](https://codeberg.org/JJSOLUTIONS/trammel-pe/issues)
- Incluye versión del navegador, sistema operativo y pasos para reproducir
- ¡Las capturas de pantalla ayudan!
- Los issues pueden ser en **Inglés o Español**

### Estilo de Código

- **Solo HTML/CSS/JS** — sin herramientas de build, sin frameworks, sin Node.js
- **Un solo archivo** — toda la app vive en `index.html`
- **Sin dependencias externas** — todo debe funcionar offline desde un solo archivo
- **Probar en múltiples navegadores** — Chrome, Firefox, Edge, Safari
- **Todo texto UI debe pasar por el sistema i18n** — sin strings hardcodeados en HTML

## Qué Necesitamos

- 🌐 **Más idiomas** — Francés, Alemán, Japonés, Mandarín, Árabe, etc.
- 🎨 **Mejoras de UI/UX** — Mejor responsividad móvil, toggle dark/light, layouts personalizables
- 📝 **Más templates** — Análisis de datos, redacción de contenido, diseño de APIs, auditoría de seguridad, planificación de proyectos
- 🧪 **Testing** — Compatibilidad de navegadores, testing de accesibilidad
- 📖 **Documentación** — Tutoriales, video walkthroughs, posts de blog
- 🔧 **Features** — Versionado de prompts, exportar a archivo, encadenamiento de prompts, integración con servidor MCP

## Código de Conducta

- Sé respetuoso y constructivo
- Enfócate en hacer Trammel PE mejor para todos
- Sin discriminación, acoso o toxicidad
- Las contribuciones en cualquier idioma son bienvenidas, pero los comentarios en código deben ser en inglés

## Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la [Licencia MIT](LICENSE).