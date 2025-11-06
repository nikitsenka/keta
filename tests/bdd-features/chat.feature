Feature: Chat Sessions and Messages
  As a user of the KETA system
  I want to create chat sessions and send messages
  So that I can interact with the knowledge extraction system

  Background: Shared document for multiple chat scenarios
    Given the API is running
    And I have created an objective with name "Product Knowledge Base"
    And I have uploaded a document with name "Product Release Info" and content "ProductY was released by CompanyX in March 2023. The product launch was announced in January 2023 and the final release occurred on March 15, 2023. CompanyX developed a new software framework called TechFrameworkX alongside ProductY. The company specializes in cloud computing and employs 500 people."
    And I have triggered extraction and waited for completion

  Scenario: Create a chat session
    When I create a chat session with the following data:
      | field        | value              |
      | name         | Research Discussion |
    Then the response status code should be 201
    And the response should contain a valid session ID
    And the chat session name should be "Research Discussion"
    And the chat session status should be "ACTIVE"

  Scenario: Send a message about product information
    Given I have created a chat session named "Product Chat"
    When I send a message with content "What software did CompanyX develop?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: Query company information from shared document
    Given I have created a chat session named "Company Info Chat"
    When I send a message with content "What information do we have about CompanyX?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: Temporal query retrieves date entities correctly
    Given I have created a chat session named "Timeline Chat"
    When I send a message with content "When was ProductY released?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should contain "2023"
    And the message content should contain date information
    And the message response should be faithful to the sources

  Scenario: Multiple questions in same chat session
    Given I have created a chat session named "Multi-Question Chat"
    When I send a message with content "What is ProductY?"
    Then the response status code should be 200
    And the message role should be "agent"
    And the message content should not be empty
    When I send a message with content "When was ProductY released?"
    Then the response status code should be 200
    And the message role should be "agent"
    And the message content should contain "2023"
    And the message content should contain date information
    When I send a message with content "Who developed ProductY?"
    Then the response status code should be 200
    And the message role should be "agent"
    And the message content should contain "CompanyX"
