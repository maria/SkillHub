Feature: Connect via Github account
 As a user
 I connect to SkillHub via my GitHub account
 In order to browse Open Source projects which may interest me
 
 
 Scenario: Connect
   Given I have a GitHub account
   When I click to sign in or log in
   And I'm redirected to GitHub
   And I approve the connection
   Then I'm redirected to SkillHub
   And I see my profile
