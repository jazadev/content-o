#**Content-o** 🤖 - Asistente de Chat Inteligente con Azure OpenAI
Es una solución empresarial de búsqueda y filtrado de contenido que ayuda y permite a las organizaciones ya sean del sector financiero, salud, producción o de servicios, ofrecer a sus empleados, asociados y terceros un punto de acceso para recibir información alineada y ajustada al ámbito de su competencia, teniendo especial atención en decantar contenido de carácter sensible, privado o confidencial, todo esto en un entorno moderno y sencillo soportado por inteligencia artificial y Azure Entity ID. 


🌟 ***Características Principales***

⚡ **Dos Niveles de Acceso**

Chat Público: Consultas generales sobre cursos
Chat Miembros: Funcionalidades exclusivas para miembros



🔐 **Seguridad**

- Autenticación mediante Microsoft Azure AD
- JWT Token validation
- Protección de endpoints sensibles



**Tecnologías**

- Backend: Flask (Python)
- Frontend: JavaScript, HTML5, CSS3
- Cloud: Azure OpenAI, Azure AD, Azure Monitor

📋 **Requisitos Previos**
```bash
python -m pip install -r requirements.txt
```


🚀 **Configuración**
Configura las variables de entorno:
```bash
AZURE_CLIENT_ID=your_client_id
   TENANT_ID=your_tenant_id
   TENANT_ID=your_tenant_id
  AZURE_OPENAI_API_KEY=your_api_key```
```

Inicia la aplicación:
```bash
python app.py
```


💡 **Características Avanzadas**

- Renderizado de Markdown
- Sistema de roles dinámico
- Monitoreo en tiempo real
- Logging integrado con Azure



🔍 **Endpoints API**

- ```/content-o-courses```: Acceso público
- ```/content-o-members```: Acceso autenticado
- ```/login/microsoft```: Autenticación Azure AD
 


📊 **Monitoreo**

- Tracking de uso de tokens
- Métricas de rendimiento
- Logs de actividad



🤝 **Contribuciones**

¡Las contribuciones son bienvenidas! Por favor, revisa nuestras guías de contribución.

📝 Licencia
MIT License

Desarrollado con ❤️ usando Azure OpenAI
