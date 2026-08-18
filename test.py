from forecast_store import (
    load_report,
    load_status,
    save_report,
    save_status,
)


save_report({
    "status": "success",
    "model_version": "1.0",
    "test": True,
})

print(load_report())


save_status({
    "status": "ready",
})

print(load_status())
