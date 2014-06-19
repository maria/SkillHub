Feature: Skills
As a user
I want to browse Open Source projects
In order to find a good fitting for contributing

  Scenario: Search for projects to fundament my skills
    Given I have some skills in <languages>
    And I want to contribute to an Open Source project
    When I click "Exercise your skills"
    Then I can see a list of projects
    And the projects are written in <top_languages>
    And I can start browsing them to find a good fit
    
    Examples:
     | languages | top_languages |
     | Python, JavaScript, HTML, CSS | Python, JavaScript, HTML |
      
  Scenario: Search for projects to enlarge my skills
    Given I have some skills in <languages>
    And I want to contribute to an Open Source project
    When I click "Extend your skills"
    Then I can see a list of projects
    And the projects are not written in <languages>
    Or the projects are written in the <last_languages> 
    And I can start browsing them to find a good fit
    
    Examples:
     | languages | last_languages |
     | Python, JavaScript, HTML, CSS | CSS,  HTML, JavaScript |
