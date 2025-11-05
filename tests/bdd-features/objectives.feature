Feature: Objectives Management
  As a user of the KETA system
  I want to manage objectives via API
  So that I can organize my knowledge extraction tasks

  Scenario: Create a new objective
    Given the API is running
    When I create an objective with the following data:
      | field       | value                                  |
      | name        | Company Analysis                       |
      | description | Extract information about companies    |
      | domain      | business                               |
    Then the response status code should be 201
    And the response should contain a valid objective ID
    And the objective name should be "Company Analysis"
    And the objective description should be "Extract information about companies"
    And the objective domain should be "business"
    And the objective status should be "DRAFT"

  Scenario: Upload a document to an objective
    Given the API is running
    And I have created an objective with name "Tech Company Research"
    When I upload a document with the following data:
      | field       | value                                                        |
      | name        | Company Overview                                             |
      | description | Overview document about EnterpriseD                          |
      | content     | EnterpriseD was founded in 2020 by FounderM in PlaceN        |
    Then the response status code should be 201
    And the response should contain a valid source ID
    And the source name should be "Company Overview"
    And the source description should be "Overview document about EnterpriseD"
    And the source extraction_status should be "PENDING"

  Scenario: Trigger extraction for a document
    Given the API is running
    And I have created an objective with name "Product Analysis"
    And I have uploaded a document with name "Product Info" and content "ProductY was released in MonthZ 2023 by CompanyK."
    When I trigger extraction for the document
    Then the response status code should be 202
    And the extraction response should contain message "Extraction triggered"
    And the extraction response should contain the source ID
    And the extraction response should contain status "PROCESSING"
