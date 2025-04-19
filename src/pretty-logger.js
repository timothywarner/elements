/**
 * pretty-logger.js - Beautified console logging with emoji support
 * 
 * Usage:
 *   const logger = require('./pretty-logger');
 *   logger.info('User logged in');
 *   logger.warn('Session expiring soon');
 *   logger.error('Failed to connect to database');
 *   logger.success('Operation completed successfully');
 *   logger.debug('Variable state:', { foo: 'bar' });
 */

const chalk = require('chalk');
const util = require('util');

// Check if chalk is installed, if not provide instructions
try {
  require.resolve('chalk');
} catch (e) {
  console.log('⚠️  Chalk is required for pretty output. Install it with:');
  console.log('npm install chalk');
  console.log('For now, falling back to basic console output.');
}

// Format objects for better readability
const formatObject = (obj) => {
  if (typeof obj !== 'object' || obj === null) return obj;
  return util.inspect(obj, { 
    colors: true, 
    depth: 5, 
    compact: false,
    breakLength: 80
  });
};

// Timestamp generator
const timestamp = () => {
  const now = new Date();
  return chalk.dim(`[${now.toISOString()}]`);
};

// Logger functions with emoji prefixes
const logger = {
  info: (...args) => {
    const messages = args.map(arg => typeof arg === 'object' ? formatObject(arg) : arg);
    console.log(`${timestamp()} ${chalk.blue('ℹ️  INFO')}    ${messages.join(' ')}`);
  },

  warn: (...args) => {
    const messages = args.map(arg => typeof arg === 'object' ? formatObject(arg) : arg);
    console.log(`${timestamp()} ${chalk.yellow('⚠️  WARNING')} ${messages.join(' ')}`);
  },

  error: (...args) => {
    const messages = args.map(arg => typeof arg === 'object' ? formatObject(arg) : arg);
    console.log(`${timestamp()} ${chalk.red('🔴 ERROR')}   ${messages.join(' ')}`);
  },

  success: (...args) => {
    const messages = args.map(arg => typeof arg === 'object' ? formatObject(arg) : arg);
    console.log(`${timestamp()} ${chalk.green('✅ SUCCESS')} ${messages.join(' ')}`);
  },

  debug: (...args) => {
    if (process.env.DEBUG !== 'true' && process.env.NODE_ENV !== 'development') return;
    
    const messages = args.map(arg => typeof arg === 'object' ? formatObject(arg) : arg);
    console.log(`${timestamp()} ${chalk.magenta('🔍 DEBUG')}   ${messages.join(' ')}`);
  },

  // Create a divider for visual separation
  divider: (title = '') => {
    const width = process.stdout.columns || 80;
    const line = '─'.repeat(width - title.length - 4);
    
    if (title) {
      console.log(chalk.dim(`┌─ ${chalk.bold(title)} ${line}`));
    } else {
      console.log(chalk.dim(`┌${'─'.repeat(width - 2)}┐`));
    }
  },

  // End a divider section
  dividerEnd: () => {
    const width = process.stdout.columns || 80;
    console.log(chalk.dim(`└${'─'.repeat(width - 2)}┘`));
  }
};

module.exports = logger; 