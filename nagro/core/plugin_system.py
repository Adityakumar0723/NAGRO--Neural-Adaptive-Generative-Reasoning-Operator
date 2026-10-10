"""
NAGRO 4.1 — Plugin System.

Extensible plugin architecture that lets users add custom tools,
agents, and capabilities without modifying core code.
"""

from __future__ import annotations
import importlib
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Plugin:
    """Represents a loaded plugin."""
    name: str
    version: str
    description: str
    author: str = ""
    tools: dict[str, Callable] = field(default_factory=dict)
    hooks: dict[str, list[Callable]] = field(default_factory=dict)
    enabled: bool = True


class PluginManager:
    """Manages NAGRO plugins — load, enable, disable, execute."""

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins: dict[str, Plugin] = {}
        self._hooks: dict[str, list[Callable]] = {}
        self._tools: dict[str, Callable] = {}

    def discover_plugins(self) -> list[str]:
        """Discover available plugins in the plugins directory."""
        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            return []

        found = []
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                found.append(item.name)
            elif item.suffix == ".py" and item.name != "__init__.py":
                found.append(item.stem)
        return found

    def load_plugin(self, name: str) -> bool:
        """Load a plugin by name."""
        plugin_path = self.plugins_dir / name

        try:
            if plugin_path.is_dir():
                spec_file = plugin_path / "__init__.py"
            else:
                spec_file = self.plugins_dir / f"{name}.py"

            if not spec_file.exists():
                return False

            # Add to sys.path temporarily
            if str(self.plugins_dir) not in sys.path:
                sys.path.insert(0, str(self.plugins_dir))

            module = importlib.import_module(name)

            plugin_info = getattr(module, "PLUGIN_INFO", {})
            plugin = Plugin(
                name=plugin_info.get("name", name),
                version=plugin_info.get("version", "1.0.0"),
                description=plugin_info.get("description", ""),
                author=plugin_info.get("author", ""),
            )

            # Register tools
            register_tools = getattr(module, "register_tools", None)
            if callable(register_tools):
                tools = register_tools()
                if isinstance(tools, dict):
                    plugin.tools = tools
                    self._tools.update(tools)

            # Register hooks
            register_hooks = getattr(module, "register_hooks", None)
            if callable(register_hooks):
                hooks = register_hooks()
                if isinstance(hooks, dict):
                    plugin.hooks = hooks
                    for event, handlers in hooks.items():
                        self._hooks.setdefault(event, []).extend(
                            handlers if isinstance(handlers, list) else [handlers]
                        )

            self.plugins[name] = plugin
            return True

        except Exception:
            return False

    def load_all(self):
        """Discover and load all available plugins."""
        for name in self.discover_plugins():
            self.load_plugin(name)

    def get_tool(self, name: str) -> Callable | None:
        """Get a registered tool by name."""
        return self._tools.get(name)

    def execute_tool(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Execute a registered tool."""
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Tool not found: {name}")
        return tool(*args, **kwargs)

    async def trigger_hook(self, event: str, **kwargs: Any) -> list[Any]:
        """Trigger all handlers for a hook event."""
        results = []
        for handler in self._hooks.get(event, []):
            try:
                result = handler(**kwargs)
                if hasattr(result, "__await__"):
                    result = await result
                results.append(result)
            except Exception:
                pass
        return results

    def list_plugins(self) -> list[dict]:
        """List all loaded plugins."""
        return [
            {
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "tools": list(p.tools.keys()),
                "hooks": list(p.hooks.keys()),
                "enabled": p.enabled,
            }
            for p in self.plugins.values()
        ]

    def list_tools(self) -> list[str]:
        """List all available tool names."""
        return list(self._tools.keys())

    def disable_plugin(self, name: str):
        if name in self.plugins:
            self.plugins[name].enabled = False
            for tool_name in self.plugins[name].tools:
                self._tools.pop(tool_name, None)

    def enable_plugin(self, name: str):
        if name in self.plugins:
            self.plugins[name].enabled = True
            self._tools.update(self.plugins[name].tools)
