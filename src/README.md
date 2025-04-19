# 🚀 Debug Utilities & Sample Applications

This directory contains debugging utilities and sample applications for the course.

## 📋 Contents

### 🔍 Debug Utilities

- **JavaScript Pretty Logger**
  - `pretty-logger.js` - Beautified console logging utility with emoji support
  - `demo.js` - Demonstration of JS logger capabilities

- **Python Pretty Logger**
  - `pretty_logger.py` - Colorful Python logging utility with emoji support
  - `demo.py` - Demonstration of Python logger with async operations

## 🛠️ Usage

### JavaScript Logger

```javascript
const logger = require('./pretty-logger');

logger.info('User logged in');
logger.warn('Session expiring soon');
logger.error('Failed to connect to database');
logger.success('Operation completed successfully');
logger.debug('Variable state:', { foo: 'bar' });

// Visual dividers
logger.divider('Section Title');
// ... your code ...
logger.dividerEnd();
```

### Python Logger

```python
from pretty_logger import logger

logger.info("User logged in")
logger.warn("Session expiring soon")
logger.error("Failed to connect to database")
logger.success("Operation completed successfully")
logger.debug("Variable state:", {"foo": "bar"})

# Visual dividers
logger.divider("Section Title")
# ... your code ...
logger.divider_end()
```

## 🚦 Running Demos

### JavaScript Demo
```bash
# Install dependencies
npm install chalk

# Run demo
node src/demo.js
```

### Python Demo
```bash
# Install dependencies (optional, for Windows)
pip install colorama

# Run demo
python src/demo.py
```

## 🔄 Debugging Support

Both utilities integrate with the VS Code launch configurations in `.vscode/launch.json`, providing:

- 🚀 Enhanced console output in debug sessions
- 🎨 Color-coded log levels with emoji indicators
- 📏 Visual dividers for separating logical sections
- 🔍 Detailed object inspection for complex data structures

## 📚 Additional Notes

- The loggers automatically detect the debug environment
- Both loggers support customization for additional log levels
- The Python logger has special support for Windows terminals via colorama
- The Node.js logger uses chalk for terminal colors 