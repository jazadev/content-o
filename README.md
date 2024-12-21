# content-o
Content-o

Content-O 🤖
Asistente de Chat Inteligente con Azure OpenAI
🌟 Características Principales
⚡ Dos Niveles de Acceso
Chat Público: Consultas generales sobre cursos
Chat Miembros: Funcionalidades exclusivas para miembros
🔐 Seguridad
Autenticación mediante Microsoft Azure AD
JWT Token validation
Protección de endpoints sensibles
🛠️ Tecnologías
Backend: Flask (Python)
Frontend: JavaScript, HTML5, CSS3
Cloud: Azure OpenAI, Azure AD, Azure Monitor
📋 Requisitos Previos
```python -m pip install -r requirements.txt```


🚀 Configuración
Configura las variables de entorno:
```AZURE_CLIENT_ID=your_client_id
   TENANT_ID=your_tenant_id
   TENANT_ID=your_tenant_id
  AZURE_OPENAI_API_KEY=your_api_key```


Inicia la aplicación:
```python app.py```

💡 Características Avanzadas
Renderizado de Markdown
Sistema de roles dinámico
Monitoreo en tiempo real
Logging integrado con Azure
🔍 Endpoints API
/content-o-courses: Acceso público
/content-o-members: Acceso autenticado
/login/microsoft: Autenticación Azure AD
📊 Monitoreo
Tracking de uso de tokens
Métricas de rendimiento
Logs de actividad
🤝 Contribuciones
¡Las contribuciones son bienvenidas! Por favor, revisa nuestras guías de contribución.

📝 Licencia
MIT License

Desarrollado con ❤️ usando Azure OpenAI
