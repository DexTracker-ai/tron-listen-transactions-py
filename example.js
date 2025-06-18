const DexTracker = require('./dex-tracker');

const tracker = new DexTracker();

tracker.on('trade', (trade) => {
  console.log('New trade:', trade);
});

tracker.on('connected', () => {
  console.log('Connected to DexTracker');
});

tracker.on('error', (error) => {
  console.error('DexTracker error:', error);
});

tracker.connect('0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00');

// Optional: Disconnect after 1 minute
setTimeout(() => {
  tracker.disconnect();
}, 60000);
