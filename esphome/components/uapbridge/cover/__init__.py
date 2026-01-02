from esphome.components import cover
import esphome.config_validation as cv
import esphome.codegen as cg
from .. import uapbridge_ns, CONF_UAPBRIDGE_ID, UAPBridge
from esphome.const import CONF_ID

DEPENDENCIES = ["uapbridge"]

UAPBridgeCover = uapbridge_ns.class_("UAPBridgeCover", cover.Cover, cg.Component)

# ESPHome >= 2025.11: cover.cover_schema(...)
# ESPHome <  2025.11: cover.COVER_SCHEMA
if hasattr(cover, "cover_schema"):
    BASE_SCHEMA = cover.cover_schema(UAPBridgeCover)
else:
    BASE_SCHEMA = cover.COVER_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(UAPBridgeCover),
        }
    )

CONFIG_SCHEMA = (
    BASE_SCHEMA.extend(
        {
            cv.GenerateID(CONF_UAPBRIDGE_ID): cv.use_id(UAPBridge),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await cover.register_cover(var, config)
    parent = await cg.get_variable(config[CONF_UAPBRIDGE_ID])
    cg.add(var.set_uapbridge_parent(parent))
