import logging
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
import datetime
import sys
import os
from dotenv import load_dotenv

load_dotenv()
# Configurar logging detallado
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_telemetry():
    """Configura la telemetría con verificación de errores"""
    try:
        connection_string = os.environ.get("TELEMETRY_CONNECTION_STRING")
        logger.debug(f"Iniciando configuración de telemetría...")
        
        # Crear y verificar el exportador
        exporter = AzureMonitorTraceExporter.from_connection_string(connection_string)
        logger.debug("Exportador creado exitosamente")
        
        # Configurar el proveedor y procesador
        provider = TracerProvider()
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        logger.debug("Telemetría configurada correctamente")
        return True
    
    except Exception as e:
        logger.error(f"Error configurando telemetría: {str(e)}", exc_info=True)
        return False

def log_action(user_id, role, query, response, content_safety_result, status, reason):
    """Registra una acción con verificación de envío"""
    try:
        logger.debug("Iniciando registro de acción...")
        
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("LogAction") as span:
            # Agregar timestamp con microsegundos para mejor trazabilidad
            current_time = datetime.datetime.utcnow()
            span.set_attribute("timestamp", current_time.isoformat() + "Z")
            span.set_attribute("user_id", user_id)
            span.set_attribute("role", role)
            span.set_attribute("query", query)
            span.set_attribute("response", response)
            span.set_attribute("content_safety_result", content_safety_result)
            span.set_attribute("status", status)
            span.set_attribute("reason", reason)
            
            # Agregar información adicional para debugging
            span.set_attribute("log_attempt_time", current_time.timestamp())
            span.set_attribute("debug_identifier", f"log_{current_time.strftime('%Y%m%d_%H%M%S_%f')}")
            
            logger.debug(f"Span creado con debug_identifier: {current_time.strftime('%Y%m%d_%H%M%S_%f')}")
        
        logger.debug("Acción registrada exitosamente")
        return True
    
    except Exception as e:
        logger.error(f"Error registrando acción: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    # Verificar la configuración de telemetría
    if setup_telemetry():
        logger.info("Configuración exitosa, procediendo con el log de prueba")
        
        # Intentar registrar una acción de prueba
        success = log_action(
            user_id="12345_test",
            role="student_test",
            query="Test query",
            response="Test response",
            content_safety_result="Test_Approved",
            status="Test_Status",
            reason="Test_Reason"
        )
        
        if success:
            logger.info("Log de prueba enviado correctamente")
            logger.info("Espera aproximadamente 2-5 minutos para que los logs aparezcan en Application Insights")
            logger.info("Busca en Application Insights usando el siguiente KQL:")
            logger.info("""
            traces
            | where customDimensions has "12345_test"
            | where timestamp > ago(1h)
            | project timestamp, customDimensions
            | order by timestamp desc
            """)
        else:
            logger.error("Fallo al enviar el log de prueba")
    else:
        logger.error("Fallo en la configuración inicial de telemetría")