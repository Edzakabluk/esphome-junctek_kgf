import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import (
    CONF_ADDRESS,
    CONF_BATTERY_LEVEL,
    CONF_CAPACITY,
    CONF_CURRENT,
    CONF_ID,
    CONF_MINUTES,
    CONF_TEMPERATURE,
    CONF_VOLTAGE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ICON_TIMER,
    ICON_FLASH,
    ICON_PERCENT,
    ICON_THERMOMETER,
    STATE_CLASS_MEASUREMENT,
    UNIT_MINUTE,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    UNIT_VOLT,
)

DEPENDENCIES = ["uart"]

AUTO_LOAD = ["sensor"]

TYPES = [
    CONF_VOLTAGE,
    CONF_CURRENT,
    CONF_BATTERY_LEVEL,
    CONF_TEMPERATURE,
    CONF_MINUTES,
    CONF_CAPACITY
]

CONF_INVERT_CURRENT = "invert_current"

JuncTekKGF = cg.global_ns.class_("JuncTekKGF", cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(JuncTekKGF),
            cv.Optional(CONF_ADDRESS, default=1): cv.int_range(1, 255),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                icon=ICON_FLASH,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon="mdi:current-dc",
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BATTERY_LEVEL): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_PERCENT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_BATTERY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_THERMOMETER,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_MINUTES): sensor.sensor_schema(
                unit_of_measurement=UNIT_MINUTE,
                icon=ICON_TIMER,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CAPACITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                icon=ICON_FLASH,
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_INVERT_CURRENT, default=False): cv.boolean,
        }
    ).extend(uart.UART_DEVICE_SCHEMA)
)


async def setup_conf(config, key, hub):
    if key in config:
        conf = config[key]
        sens = await sensor.new_sensor(conf)
        cg.add(getattr(hub, f"set_{key}_sensor")(sens))


async def to_code(config):
    var = cg.new_Pvariable(
        config[CONF_ID], config[CONF_ADDRESS], config[CONF_INVERT_CURRENT]
    )
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
    for key in TYPES:
        await setup_conf(config, key, var)
