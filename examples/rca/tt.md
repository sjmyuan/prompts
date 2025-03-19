**Problem Definition**: You want to change your branching policy from GitHub Flow to Trunk-Based Development to improve integration and deployment frequency, decrease conflict resolution effort, simplify the deployment process, and avoid blocking deployments. However, the change is not possible because the QA team disagrees with merging untested code to the master branch and deploying uncompleted features to production, and device tests cannot be automated.

**Data**:
- Development team size: 5 developers
- QA team size: 2 QA engineers
- Tools and technologies: Java, Cypress, GitHub Actions
- Device tests automation is not possible due to the lack of off-the-shelf techniques, and the team doesn't have the time to develop custom techniques.
- Deployment frequency: 1-2 months
- Time from development to production: more than 1 month
- Devices involved in tests: sensitive data hardware

**Root Causes**:
1. The QA team's concerns about merging untested code and deploying uncompleted features to production are preventing the change to Trunk-Based Development.
2. Lack of time and knowledge to develop custom techniques for automating device tests.
3. Lack of confidence in using feature toggles to ensure the stability of production.

**Suggested Actions**:
1. Educate the team about the benefits of Trunk-Based Development and address their concerns by implementing best practices, such as using feature flags and maintaining a stable master branch through continuous integration and testing.
2. Allocate time and resources to research and develop custom techniques for automating device tests or explore third-party solutions that could help automate these tests.
3. Investigate and learn from successful implementations of feature toggles in similar projects or industries to build confidence in using them to ensure production stability.

**Questions and Answers**:

1. Q: Why does the QA team disagree with merging untested code to the master branch and deploying uncompleted features to production?
   A: They want to keep the master branch deployable and don't want the uncompleted feature to affect the features on production.

2. Q: Why is there no time to develop custom techniques for automating device tests?
   A: It needs a huge effort, and the team doesn't know how to do it right now.

3. Q: Why haven't alternative branching strategies, such as feature toggles or environment-specific branches, been considered to address the QA team's concerns?
   A: The team wants to use feature toggles but doesn't have enough confidence to say it can ensure the stability of production.