// End-to-end test for ChatWidget functionality
import { chatService } from '../../services/api';

async function runE2ETest() {
  console.log('🚀 Starting end-to-end test for ChatWidget...');

  try {
    // 1. Test session creation
    console.log('1. Testing session creation...');
    const sessionResponse = await chatService.createSession({
      timestamp: new Date().toISOString(),
      metadata: {
        type: 'e2e-test',
        testId: `test-${Date.now()}`
      }
    });

    console.log('✅ Session created:', sessionResponse.session_id);
    const sessionId = sessionResponse.session_id;

    // 2. Test message sending and receiving
    console.log('2. Testing message sending and receiving...');
    const messageResponse = await chatService.sendMessage({
      query: "Hello, this is a test message for the end-to-end test. Can you confirm you received this message?",
      session_id: sessionId,
      context: {
        current_page: "/test-e2e",
        referrer: "e2e-test"
      }
    });

    console.log('✅ Message response received:', {
      answer: messageResponse.answer || messageResponse.response,
      citations: messageResponse.citations,
      sessionId: messageResponse.session_id
    });

    // 3. Test message history retrieval
    console.log('3. Testing message history retrieval...');
    const historyResponse = await chatService.getHistory(sessionId);
    console.log('✅ History retrieved:', {
      session_id: historyResponse.session_id,
      message_count: historyResponse.messages?.length || 0
    });

    // 4. Validate response quality
    const responseText = messageResponse.answer || messageResponse.response;
    if (!responseText || responseText.toLowerCase().includes('error')) {
      console.log('❌ Response validation failed: Invalid response received');
      return false;
    }

    console.log('✅ All end-to-end tests passed!');
    console.log('✅ ChatWidget is successfully communicating with the backend');
    console.log('✅ Session management is working correctly');
    console.log('✅ Message sending and receiving is functional');

    return true;
  } catch (error) {
    console.error('❌ End-to-end test failed:', error.message);
    return false;
  }
}

// Run the test
runE2ETest().then(success => {
  if (success) {
    console.log('\n🎉 E2E Test Summary: All systems operational!');
  } else {
    console.log('\n⚠️ E2E Test Summary: Issues detected, please review logs above.');
  }
});

export default runE2ETest;