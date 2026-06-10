from .main import router as router_main
from .profile import router as router_prof
from .company import router as router_comp
from .task import router as router_task
from .employee import router as router_emp

ROUTERS = [router_main, router_prof, router_comp, router_task, router_emp]