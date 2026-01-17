"""
Tests for modular_app_structure.py

Tests cover:
- EventSystem class
- ConfigManager class
- ModuleRegistry class
- ModuleInterface (abstract class behavior)
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modular_app_structure import EventSystem, ConfigManager, ModuleInterface, ModuleRegistry


class TestEventSystem:
    """Tests for the EventSystem class."""

    def test_init_creates_empty_handlers(self, event_system):
        """Should initialize with empty event handlers."""
        assert hasattr(event_system, '_event_handlers')
        assert isinstance(event_system._event_handlers, dict)

    def test_register_handler(self, event_system):
        """Should register event handler."""
        handler_called = []

        def handler(event_type, data):
            handler_called.append((event_type, data))

        event_system.register_handler('test_event', handler)
        event_system.emit_event('test_event', {'key': 'value'})

        assert len(handler_called) == 1
        assert handler_called[0] == ('test_event', {'key': 'value'})

    def test_register_multiple_handlers(self, event_system):
        """Should register multiple handlers for same event."""
        results = []

        def handler1(event_type, data):
            results.append('handler1')

        def handler2(event_type, data):
            results.append('handler2')

        event_system.register_handler('test', handler1)
        event_system.register_handler('test', handler2)
        event_system.emit_event('test', {})

        assert results == ['handler1', 'handler2']

    def test_unregister_handler(self, event_system):
        """Should unregister event handler."""
        handler_called = []

        def handler(event_type, data):
            handler_called.append(data)

        event_system.register_handler('test_event', handler)
        result = event_system.unregister_handler('test_event', handler)
        event_system.emit_event('test_event', {})

        assert result is True
        assert len(handler_called) == 0

    def test_unregister_nonexistent_handler(self, event_system):
        """Should return False when unregistering nonexistent handler."""

        def handler(event_type, data):
            pass

        result = event_system.unregister_handler('nonexistent_event', handler)
        assert result is False

    def test_emit_without_handlers(self, event_system):
        """Should not raise error when emitting event without handlers."""
        # Should not raise
        event_system.emit_event('no_handlers', {'data': 123})

    def test_emit_with_none_data(self, event_system):
        """Should handle None event data."""
        handler_called = []

        def handler(event_type, data):
            handler_called.append(data)

        event_system.register_handler('test', handler)
        event_system.emit_event('test')  # No data argument

        assert len(handler_called) == 1
        assert handler_called[0] == {}  # Default empty dict

    def test_handler_exception_isolation(self, event_system):
        """Exception in one handler should not affect others."""
        results = []

        def bad_handler(event_type, data):
            raise ValueError("Test error")

        def good_handler(event_type, data):
            results.append('success')

        event_system.register_handler('test', bad_handler)
        event_system.register_handler('test', good_handler)

        # Should not raise, and good_handler should still be called
        event_system.emit_event('test', {})

        assert 'success' in results

    def test_multiple_event_types(self, event_system):
        """Should handle multiple event types independently."""
        results = []

        def handler_a(event_type, data):
            results.append(f'a:{event_type}')

        def handler_b(event_type, data):
            results.append(f'b:{event_type}')

        event_system.register_handler('event_a', handler_a)
        event_system.register_handler('event_b', handler_b)

        event_system.emit_event('event_a', {})
        event_system.emit_event('event_b', {})

        assert 'a:event_a' in results
        assert 'b:event_b' in results
        assert len(results) == 2


class TestConfigManager:
    """Tests for the ConfigManager class."""

    def test_load_config_from_file(self, temp_config_file):
        """Should load config from file."""
        manager = ConfigManager(temp_config_file)
        assert manager.get_config('app', 'name') == 'Test App'

    def test_default_config_on_missing_file(self):
        """Should use defaults when file is missing."""
        manager = ConfigManager('nonexistent_file.json')
        # Should have default app name
        assert manager.get_config('app', 'name') == 'FractalSense EntaENGELment'

    def test_get_config_full(self, temp_config_file):
        """Should return full config when no args."""
        manager = ConfigManager(temp_config_file)
        config = manager.get_config()
        assert isinstance(config, dict)
        assert 'app' in config

    def test_get_config_section(self, temp_config_file):
        """Should return section config."""
        manager = ConfigManager(temp_config_file)
        app_config = manager.get_config('app')
        assert app_config is not None
        assert 'name' in app_config

    def test_get_config_key(self, temp_config_file):
        """Should return specific key value."""
        manager = ConfigManager(temp_config_file)
        name = manager.get_config('app', 'name')
        assert name == 'Test App'

    def test_get_config_nonexistent_section(self, temp_config_file):
        """Should return None for nonexistent section."""
        manager = ConfigManager(temp_config_file)
        result = manager.get_config('nonexistent_section')
        assert result is None

    def test_get_config_nonexistent_key(self, temp_config_file):
        """Should return None for nonexistent key."""
        manager = ConfigManager(temp_config_file)
        result = manager.get_config('app', 'nonexistent_key')
        assert result is None

    def test_set_config(self, temp_config_file):
        """Should update config values."""
        manager = ConfigManager(temp_config_file)
        manager.set_config('app', 'version', '2.0.0')
        assert manager.get_config('app', 'version') == '2.0.0'

    def test_set_config_new_section(self, temp_config_file):
        """Should create new section if needed."""
        manager = ConfigManager(temp_config_file)
        manager.set_config('new_section', 'key', 'value')
        assert manager.get_config('new_section', 'key') == 'value'

    def test_get_module_config(self, temp_config_file):
        """Should return module-specific config."""
        manager = ConfigManager(temp_config_file)
        module_config = manager.get_module_config('TestModule')
        assert module_config.get('enabled') is True
        assert module_config.get('setting1') == 'value1'

    def test_get_module_config_nonexistent(self, temp_config_file):
        """Should return empty dict for nonexistent module."""
        manager = ConfigManager(temp_config_file)
        module_config = manager.get_module_config('NonexistentModule')
        assert module_config == {}

    def test_set_module_config(self, temp_config_file):
        """Should set module-specific config."""
        manager = ConfigManager(temp_config_file)
        manager.set_module_config('NewModule', {'enabled': True, 'setting': 'test'})

        module_config = manager.get_module_config('NewModule')
        assert module_config['enabled'] is True
        assert module_config['setting'] == 'test'

    def test_save_config(self, temp_config_file):
        """Should save config to file."""
        manager = ConfigManager(temp_config_file)
        manager.set_config('app', 'test_key', 'test_value')

        result = manager.save_config()
        assert result is True

        # Reload and verify
        manager2 = ConfigManager(temp_config_file)
        assert manager2.get_config('app', 'test_key') == 'test_value'


class TestModuleInterface:
    """Tests for the ModuleInterface abstract class."""

    def test_cannot_instantiate_directly(self):
        """Should not be able to instantiate ModuleInterface directly."""
        with pytest.raises(TypeError):
            ModuleInterface()

    def test_subclass_must_implement_methods(self):
        """Subclass must implement all abstract methods."""

        class IncompleteModule(ModuleInterface):
            pass

        with pytest.raises(TypeError):
            IncompleteModule()

    def test_complete_subclass(self):
        """Complete subclass should be instantiable."""

        class CompleteModule(ModuleInterface):
            def initialize(self, app_context):
                return True

            def process(self, input_data):
                return {}

            def get_ui_components(self):
                return {}

            def cleanup(self):
                pass

            @property
            def name(self):
                return "TestModule"

            @property
            def version(self):
                return "1.0.0"

            @property
            def description(self):
                return "Test module"

            @property
            def dependencies(self):
                return []

        module = CompleteModule()
        assert module.name == "TestModule"
        assert module.version == "1.0.0"


class TestModuleRegistry:
    """Tests for the ModuleRegistry class."""

    def test_init_creates_empty_registries(self):
        """Should initialize with empty registries."""
        registry = ModuleRegistry()
        assert registry._modules == {}
        assert registry._module_classes == {}

    def test_get_module_nonexistent(self):
        """Should return None for nonexistent module."""
        registry = ModuleRegistry()
        result = registry.get_module('nonexistent')
        assert result is None

    def test_get_all_modules_empty(self):
        """Should return empty dict when no modules."""
        registry = ModuleRegistry()
        modules = registry.get_all_modules()
        assert modules == {}

    def test_discover_modules_nonexistent_dir(self):
        """Should return 0 for nonexistent directory."""
        registry = ModuleRegistry()
        count = registry.discover_modules('/nonexistent/path')
        assert count == 0


class MockModule(ModuleInterface):
    """Mock module for testing."""

    _name = "MockModule"
    _version = "1.0.0"
    _description = "Mock module for testing"
    _dependencies = []

    def __init__(self, name=None, deps=None):
        if name:
            self._name = name
        if deps:
            self._dependencies = deps

    def initialize(self, app_context):
        return True

    def process(self, input_data):
        return input_data

    def get_ui_components(self):
        return {}

    def cleanup(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    @property
    def description(self):
        return self._description

    @property
    def dependencies(self):
        return self._dependencies


class TestModuleRegistryWithMocks:
    """Tests for ModuleRegistry using mock modules."""

    def test_register_module_class(self):
        """Should register a module class."""
        registry = ModuleRegistry()

        result = registry.register_module_class(MockModule, '/path/to/module')
        assert result is True
        assert 'MockModule' in registry._module_classes

    def test_register_duplicate_module(self):
        """Should not register duplicate module."""
        registry = ModuleRegistry()

        registry.register_module_class(MockModule, '/path/to/module')
        result = registry.register_module_class(MockModule, '/path/to/module')

        assert result is False

    def test_initialize_modules(self):
        """Should initialize registered modules."""
        registry = ModuleRegistry()
        registry.register_module_class(MockModule, '/path/to/module')

        result = registry.initialize_modules({'app': 'context'})

        assert result is True
        assert 'MockModule' in registry._modules

    def test_get_module_after_init(self):
        """Should return module after initialization."""
        registry = ModuleRegistry()
        registry.register_module_class(MockModule, '/path/to/module')
        registry.initialize_modules({})

        module = registry.get_module('MockModule')

        assert module is not None
        assert module.name == 'MockModule'

    def test_cleanup_modules(self):
        """Should cleanup all modules."""
        registry = ModuleRegistry()
        registry.register_module_class(MockModule, '/path/to/module')
        registry.initialize_modules({})

        # Should not raise
        registry.cleanup_modules()

        # Modules should be cleared
        assert registry._modules == {}


class TestModuleDependencyResolution:
    """Tests for module dependency resolution."""

    def test_determine_load_order_single_module(self):
        """Should handle single module without dependencies."""
        registry = ModuleRegistry()

        class SingleModule(MockModule):
            _name = "SingleModule"
            _dependencies = []

        registry.register_module_class(SingleModule, '/path')
        registry._determine_load_order()

        assert 'SingleModule' in registry._module_load_order

    def test_determine_load_order_with_dependencies(self):
        """Should order modules by dependencies."""
        registry = ModuleRegistry()

        class ModuleA(MockModule):
            _name = "ModuleA"
            _dependencies = []

        class ModuleB(MockModule):
            _name = "ModuleB"
            _dependencies = ["ModuleA"]

        # Register in wrong order
        registry.register_module_class(ModuleB, '/path')
        registry.register_module_class(ModuleA, '/path')

        registry._determine_load_order()

        # ModuleA should come before ModuleB
        order = registry._module_load_order
        assert order.index('ModuleA') < order.index('ModuleB')

    def test_cyclic_dependency_detection(self):
        """Should detect cyclic dependencies."""
        registry = ModuleRegistry()

        class ModuleX(MockModule):
            _name = "ModuleX"
            _dependencies = ["ModuleY"]

        class ModuleY(MockModule):
            _name = "ModuleY"
            _dependencies = ["ModuleX"]

        registry.register_module_class(ModuleX, '/path')
        registry.register_module_class(ModuleY, '/path')

        with pytest.raises(ValueError, match="Zyklische Abhängigkeit"):
            registry._determine_load_order()

    def test_missing_dependency_warning(self):
        """Should handle missing dependencies gracefully."""
        registry = ModuleRegistry()

        class ModuleWithMissing(MockModule):
            _name = "ModuleWithMissing"
            _dependencies = ["NonexistentModule"]

        registry.register_module_class(ModuleWithMissing, '/path')

        # Should not raise, just warn
        registry._determine_load_order()

        assert 'ModuleWithMissing' in registry._module_load_order


class TestConfigManagerEdgeCases:
    """Edge case tests for ConfigManager."""

    def test_invalid_json_file(self, tmp_path):
        """Should handle invalid JSON file."""
        invalid_file = tmp_path / 'invalid.json'
        invalid_file.write_text('not valid json {{{')

        manager = ConfigManager(str(invalid_file))

        # Should fall back to defaults
        assert manager.get_config('app', 'name') == 'FractalSense EntaENGELment'

    def test_nested_config_update(self, temp_config_file):
        """Should handle nested config updates."""
        manager = ConfigManager(temp_config_file)

        # Set nested value
        manager.set_config('modules', 'TestModule', {'nested': 'value'})

        # Original app config should still exist
        assert manager.get_config('app', 'name') == 'Test App'

    def test_empty_config_file(self, tmp_path):
        """Should handle empty config file."""
        empty_file = tmp_path / 'empty.json'
        empty_file.write_text('{}')

        manager = ConfigManager(str(empty_file))

        # Should have defaults
        assert manager.get_config('app') is not None


class TestEventSystemEdgeCases:
    """Edge case tests for EventSystem."""

    def test_handler_with_complex_data(self, event_system):
        """Should handle complex event data."""
        received_data = []

        def handler(event_type, data):
            received_data.append(data)

        event_system.register_handler('complex', handler)

        complex_data = {
            'nested': {'deep': {'value': 123}},
            'list': [1, 2, 3],
            'none': None
        }

        event_system.emit_event('complex', complex_data)

        assert received_data[0] == complex_data

    def test_same_handler_multiple_events(self, event_system):
        """Should allow same handler for multiple events."""
        call_count = [0]

        def handler(event_type, data):
            call_count[0] += 1

        event_system.register_handler('event1', handler)
        event_system.register_handler('event2', handler)

        event_system.emit_event('event1', {})
        event_system.emit_event('event2', {})

        assert call_count[0] == 2

    def test_unregister_from_different_event(self, event_system):
        """Should not affect other events when unregistering."""
        results = []

        def handler(event_type, data):
            results.append(event_type)

        event_system.register_handler('event1', handler)
        event_system.register_handler('event2', handler)

        event_system.unregister_handler('event1', handler)

        event_system.emit_event('event1', {})
        event_system.emit_event('event2', {})

        assert 'event1' not in results
        assert 'event2' in results
