from lettuce import step


@step("Given I have some skills in (\w)")
def skill_step(step, languages):
  pass
@step("And I want to contribute to an Open Source project")
def skill_step(step):
  pass
@step('When I click "Exercise your skills"')
def skill_step(step):
  pass
@step("Then I can see a list of projects")
def skill_step(step):
  pass
@step("And the projects are written in (\w)")
def skill_step(step, top_languages):
  pass
@step("And I can start browsing them to find a good fit")
def skill_step(step):
  pass
@step("Given I have some skills in (\w)")
def skill_step(step, languages):
  pass
@step("And I want to contribute to an Open Source project")
def skill_step(step):
  pass
@step('When I click "Extend your skills"')
def skill_step(step):
  pass
@step("Then I can see a list of projects")
def skill_step(step):
  pass
@step("And the projects are not written in (\w)")
def skill_step(step, languages):
  pass
@step("Or the projects are written in the (\w)")
def skill_step(step, last_languages):
  pass
@step("And I can start browsing them to find a good fit")
def skill_step(step):
  pass
