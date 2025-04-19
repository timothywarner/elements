/**
 * demo.js - Demonstration of pretty-logger
 * 
 * Run with:
 *   node src/demo.js
 */

const logger = require('./pretty-logger');

// Demo function to show off the logger capabilities
async function loggerDemo() {
  logger.divider('💫 LOGGER DEMO');
  
  logger.info('Starting application...');
  
  // Simulate processing with a small delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  logger.debug('Config loaded', {
    environment: 'development',
    features: {
      auth: true,
      analytics: false,
      darkMode: true
    },
    version: '1.0.0'
  });
  
  await new Promise(resolve => setTimeout(resolve, 500));
  
  logger.success('Connected to database');
  
  await new Promise(resolve => setTimeout(resolve, 500));
  
  logger.warn('Cache miss for user profile');
  
  await new Promise(resolve => setTimeout(resolve, 500));
  
  try {
    // Simulate an error
    throw new Error('Failed to process payment');
  } catch (error) {
    logger.error('Payment processing failed', { 
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
  
  await new Promise(resolve => setTimeout(resolve, 500));
  
  logger.info('Processing complete');
  
  logger.dividerEnd();
}

// Run the demo
loggerDemo(); 