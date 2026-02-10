 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/proyect/alembic/script.py.mako b/proyect/alembic/script.py.mako
new file mode 100644
index 0000000000000000000000000000000000000000..79ccc888c15fd23ab2538bf1553ec4470643ba04
--- /dev/null
+++ b/proyect/alembic/script.py.mako
@@ -0,0 +1,25 @@
+"""${message}
+
+Revision ID: ${up_revision}
+Revises: ${down_revision | comma,n}
+Create Date: ${create_date}
+"""
+from __future__ import annotations
+
+from alembic import op
+import sqlalchemy as sa
+${imports if imports else ""}
+
+# revision identifiers, used by Alembic.
+revision = ${repr(up_revision)}
+down_revision = ${repr(down_revision)}
+branch_labels = ${repr(branch_labels)}
+depends_on = ${repr(depends_on)}
+
+
+def upgrade() -> None:
+    ${upgrades if upgrades else "pass"}
+
+
+def downgrade() -> None:
+    ${downgrades if downgrades else "pass"}
 
EOF
)
