from misc.db import Connection
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.handlers import (
    error_404, 
    error_400_with_detail, 
    error_500
)
from misc.sound_templates import sound_processing

from models.sound_template import (
    SoundProcessingFilters, 
    BaseTemplateReturn,
    BaseConfigGain
)
from models.sound_template_meta import MetaTemplate

from db import radios as radios_db
from db import sound_template as template_db

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/sound_templates",
    tags=['sound_templates']
)


@router.get("/import/{name}", response_model=BaseTemplateReturn)
async def import_by_id(
    name: str,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
)-> JSONResponse:
    """
    Load template(cfg) file from template directory 
    by template {name}, parse it and load to db as json.
    """
    template = {}
    for filter in SoundProcessingFilters:
        presets_dir = conf["sound_processing"]["presets_dir"]
        config = sound_processing.from_file_to_dict(filter.value, presets_dir, preset=name)
        if config:
            template[filter.name] = config
    if not template:
        return await error_404(f"unbale to found template {name}")
    return await template_db.import_template(conn, name, template)


@router.get("/meta/{radio_id}", response_model=MetaTemplate)
async def get_meta_template(
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
)-> JSONResponse:
    """
    Load sound processing config from db by {radio_id} 
    and merge(add correct value from config to each filter params and items) 
    it with meta audio processing template if
    config exists else radio processing template instead.
    """
    radio_data = await radios_db.get_sound_processing_data(conn, radio_id)
    gain_out = conf["sound_processing"]["default_gain"]
    if not radio_data:
        return await error_404(f"radio with id {radio_id} not found")
    if radio_data.sound_processing_config.gain_out:
        gain_out = radio_data.sound_processing_config.gain_out
    if radio_data.sound_processing_config.config:
        config = radio_data.sound_processing_config.config
    else:
        template = await template_db.get_template(
            conn, 
            radio_data.sound_processing_template
        )
        if not template:
            return await error_404(f"""unable to found sound 
            processing template {radio_data.sound_processing_template}""")
        config = template.config
    new_meta_config = sound_processing.get_meta_config(config, conf["sound_processing"]["meta_template"])
    return {
        "config": new_meta_config,
        "preset": radio_data.sound_processing_template,
        "gain_out": gain_out
    }


@router.post("/meta/{radio_id}", response_model=MetaTemplate)
async def update_config(
    body: BaseConfigGain,
    radio_id: int,
    conn: Connection = Depends(get_db),
    conf: dict = Depends(get_conf)
)-> JSONResponse:
    """
    Update current radio config and return merge of it
    and meta template

    You can specify {"config": {}} to empty it.
    """
    meta_config_path = conf["sound_processing"]["meta_template"]
    config = sound_processing.validate_config(body.config,  meta_config_path)
    body.config = config
    radio_data = await radios_db.update_sound_processing_config(
        body.dict(), 
        conn,
        radio_id
    )
    if not radio_data:
        return await error_404("unable to found radio")
    config = body.config
    template = await template_db.get_template(conn, radio_data.sound_processing_template)
    if not template:
        return await error_500(f"""unable to found sound processing template
                               {radio_data.sound_processing_template}""")
    merged_config = sound_processing.merge_configs(template.config, config)
    plugins_str = sound_processing.to_gstreamer_plugins(merged_config)
    new_meta_config = sound_processing.get_meta_config(config, meta_config_path)
    return {
        "config": new_meta_config,
        "preset": radio_data.sound_processing_template,
        "gain_out": radio_data.sound_processing_config.gain_out
    }
