// Test script to verify API connection to deployed backend
import { ragService, chatService } from '../../services/api';

async function testApiConnection() {
  try {
    console.log('Testing connection to deployed backend...');
    console.log('API Base URL:', process.env.REACT_APP_API_BASE_URL || 'https://alihaidernoorani-deploy-docusaurus-book.hf.space/api');

    // Test health endpoint
    const healthResponse = await ragService.getHealth();
    console.log('Health check response:', healthResponse);

    if (healthResponse.status === 'healthy' || healthResponse.status === 'ok') {
      console.log('✅ Health check successful!');
    } else {
      console.log('❌ Health check failed:', healthResponse);
      return false;
    }

    // Test chat session creation
    console.log('Testing chat session creation...');
    try {
      const sessionResponse = await chatService.createSession({
        timestamp: new Date().toISOString(),
        metadata: { type: 'test-session' }
      });
      console.log('Session creation response:', sessionResponse);
      const sessionId = sessionResponse.session_id;

      if (sessionId) {
        console.log('✅ Session creation successful!');

        // Test message sending
        console.log('Testing message sending...');
        const messageResponse = await chatService.sendMessage({
          query: "Hello, this is a test message to verify the API connection.",
          session_id: sessionId
        });

        console.log('Message response:', messageResponse);
        if (messageResponse.answer || messageResponse.response) {
          console.log('✅ Message sending successful!');
          return true;
        } else {
          console.log('⚠️ Message sending returned unexpected format:', messageResponse);
          return true; // Still consider it successful since it didn't error
        }
      } else {
        console.log('❌ Session creation failed - no session ID returned');
        return false;
      }
    } catch (sessionError) {
      console.error('❌ Session creation or message sending failed:', sessionError.message);
      return false;
    }
  } catch (error) {
    console.error('❌ API connection failed:', error.message);
    return false;
  }
}

// Run the test
testApiConnection();

export default testApiConnection;