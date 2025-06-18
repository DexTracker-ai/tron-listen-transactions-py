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

tracker.connect('sol', '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R');

// Optional: Disconnect after 1 minute
setTimeout(() => {
  tracker.disconnect();
}, 60000);
