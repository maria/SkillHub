Feature: Mentoring
As a user
I want to get some insights 
In order to start my first contribution


  Scenario: Tips list
    Given I connected to SkillHub
    And I'm on the Home page
    And I can see a list of tips
    When I search for projects
    Then I can relate to those steps
    And I can start contributing to a project
  
  Scenario: Tutorials
    Given I want to learn a new technology
    When I browse the tutorials page
    Then I can find a list of resources
    And I can start learning through a tutorial
    And find a project to contribute
