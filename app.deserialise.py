from ytd_api.clients import *
from ytd_api.raw_models import ResponseContext

channel_id: str = "UC8Yu1_yfN5qPh601Y4btsYw"  # Arctic Monkeys

data: dict = WEB_REMIX.adaptor.dispatch("browse", body={"browseId": channel_id})
# data: dict = WEB.adaptor.dispatch("browse", body={"browseId": channel_id})

d=data

rc = ResponseContext.parse_obj(data["responseContext"])
