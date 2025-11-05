Feature: Chat Sessions and Messages
  As a user of the KETA system
  I want to create chat sessions and send messages
  So that I can interact with the knowledge extraction system

  Scenario: Create a chat session
    Given the API is running
    And I have created an objective with name "AI Research"
    When I create a chat session with the following data:
      | field        | value              |
      | name         | Research Discussion |
    Then the response status code should be 201
    And the response should contain a valid session ID
    And the chat session name should be "Research Discussion"
    And the chat session status should be "ACTIVE"

  Scenario: Send a message in a chat session
    Given the API is running
    And I have created an objective with name "Tech Research"
    And I have uploaded a document with name "Tech Doc" and content "CompanyA developed a new software framework called TechFrameworkX in 2023"
    And I have created a chat session named "Tech Chat"
    When I send a message with content "What software did CompanyA develop?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: Agent responds to question about uploaded document
    Given the API is running
    And I have created an objective with name "Business Intelligence"
    And I have uploaded a document with name "Company Profile" and content "OrganizationB was founded in 2020 by PersonX in CityY. The company specializes in cloud computing and employs 500 people."
    And I have created a chat session named "Company Chat"
    When I send a message with content "What information do we have about OrganizationB?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources

  Scenario: Extraction completes successfully with generic entities
    Given the API is running
    And I have created an objective with name "Company Knowledge Base"
    And I have uploaded a document with name "Company Info" and content "CorporationC was founded by PersonA in LocationZ. The company focuses on manufacturing ProductX and has operations in RegionY."
    And I have triggered extraction and waited for completion
    And I have created a chat session named "Knowledge Chat"
    When I send a message with content "What do you know about companies?"
    Then the response status code should be 200
    And the response should contain a valid message ID
    And the message role should be "agent"
    And the message content should not be empty
    And the message response should be faithful to the sources
