from queries.orm import SyncOrm
from queries.core import SyncCore

SyncOrm.create_tables()
SyncOrm.sync_insert_user()

SyncOrm.sync_update_user()
# SyncOrm.sync_get_user()

