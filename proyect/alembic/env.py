 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/proyect/alembic/env.py b/proyect/alembic/env.py
new file mode 100644
index 0000000000000000000000000000000000000000..5fb2cd8544e2103867547d21cb24ce3c04a76ef3
--- /dev/null
+++ b/proyect/alembic/env.py
@@ -0,0 +1,58 @@
+from __future__ import annotations
+
+from logging.config import fileConfig
+import os
+
+from alembic import context
+from sqlalchemy import engine_from_config, pool
+
+from app.db.session import Base
+import app.db.models  # noqa: F401
+
+config = context.config
+
+if config.config_file_name is not None:
+    fileConfig(config.config_file_name)
+
+
+def _database_url() -> str:
+    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
+
+
+target_metadata = Base.metadata
+
+
+def run_migrations_offline() -> None:
+    url = _database_url()
+    context.configure(
+        url=url,
+        target_metadata=target_metadata,
+        literal_binds=True,
+        dialect_opts={"paramstyle": "named"},
+    )
+
+    with context.begin_transaction():
+        context.run_migrations()
+
+
+def run_migrations_online() -> None:
+    configuration = config.get_section(config.config_ini_section, {})
+    configuration["sqlalchemy.url"] = _database_url()
+
+    connectable = engine_from_config(
+        configuration,
+        prefix="sqlalchemy.",
+        poolclass=pool.NullPool,
+    )
+
+    with connectable.connect() as connection:
+        context.configure(connection=connection, target_metadata=target_metadata)
+
+        with context.begin_transaction():
+            context.run_migrations()
+
+
+if context.is_offline_mode():
+    run_migrations_offline()
+else:
+    run_migrations_online()
 
EOF
)
