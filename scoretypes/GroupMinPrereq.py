# Developed by Marszpace
# Most of the code here is taken from GroupMin, builtin of CMS.
# Comments are re-written as see fit for users of CMS who are
# competitive programmers themselves. You are encouraged to read
# the codebase of CMS through github if you do not understand
# parts of the code, particularly about which functions are used.
# 
# Any feedback (including clarity of comment and code) is greatly
# appreciated by this beginner developer.
#
# This work falls under GNU Affero General Public License, same as CMS.

from cms.grading.scoretypes import ScoreTypeGroup # This assumes CMS is 'installed' into the system

# Dummy function to mark translatable string.
def N_(message):
    return message


class GroupMinPrereq(ScoreTypeGroup):
    """The score of a submission is the sum of the product of the
    minimum of the score of each testcases within a range, as well
    as their prerequisites, with the multiplier within each range.

    In particaluar, it should function as if we put every testcase 
    from prerequisites into a subtask/group/range.

    Parameters are ["Display", [m, t, [p1, p2, ..., pi]], ... ]. prerequisite 
    are *one-based* indexed. "Display" parameter must be either "None" or "All",
    which tells CMS how to display the task outcome.
    """

    def compute_score(self, submission_result):
        """See ScoreType.compute_score."""
        # Actually, this means it didn't even compile!
        if not submission_result.evaluated():
            return 0.0, [], 0.0, [], ["%lg" % 0.0 for _ in self.parameters]

        score = 0
        subtasks = []
        public_score = 0
        public_subtasks = []
        ranking_details = []
        prereq = []

        # Generate the complete prerequisite table
        for st_idx, parameter in enumerate(self.parameters):
            thisPrereq = set()
            for pr_idx in parameter[2]:
                thisPrereq.update(prereq[pr_idx])
            prereq.append(thisPrereq)

        targets = self.retrieve_target_testcases()
        evaluations = {ev.codename: ev for ev in submission_result.evaluations}

        for st_idx, parameter in enumerate(self.parameters):
            target = []
            if(self.parameters == "All"):
                for pr_idx in sorted(prereq):
                    target.append(targets[pr_idx-1])

            target.append(targets[st_idx])
            testcases = []
            public_testcases = []
            previous_tc_all_correct = True
            for tc_idx in target:
                tc_outcome = self.get_public_outcome(
                    float(evaluations[tc_idx].outcome), parameter)

                testcases.append({
                    "idx": tc_idx,
                    "outcome": tc_outcome,
                    "text": evaluations[tc_idx].text,
                    "time": evaluations[tc_idx].execution_time,
                    "memory": evaluations[tc_idx].execution_memory,
                    "show_in_restricted_feedback": previous_tc_all_correct})
                if self.public_testcases[tc_idx]:
                    public_testcases.append(testcases[-1])
                    # Only block restricted feedback if this is the first
                    # *public* non-correct testcase, otherwise we might be
                    # leaking info on private testcases.
                    if tc_outcome != "Correct":
                        previous_tc_all_correct = False
                else:
                    public_testcases.append({"idx": tc_idx})

            st_score_fraction = self.reduce(
                [float(evaluations[tc_idx].outcome) for tc_idx in target],
                parameter)

            ### BEGIN Prerequisite Grading Part 

            """
            This part assumes that the given parameters are valid (the admin is 
            responsible for asserting this), and that for each subtask, its
            prerequisite are strictly before it, i.e. that 1...n is a valid 
            grading sequence.
            """
            for pr_idx in parameter[2]:
                pr_score_fraction = subtasks[pr_idx - 1].get("score_fraction")
                st_score_fraction = min(st_score_fraction, pr_score_fraction)
            ### END Prerequisite Grading Part

            st_score = st_score_fraction * parameter[0]

            score += st_score
            subtasks.append({
                "idx": st_idx + 1,
                # We store the fraction so that an "example" testcase
                # with a max score of zero is still properly rendered as
                # correct or incorrect.
                "score_fraction": st_score_fraction,
                "max_score": parameter[0],
                "testcases": testcases})
            if all(self.public_testcases[tc_idx] for tc_idx in target):
                public_score += st_score
                public_subtasks.append(subtasks[-1])
            else:
                public_subtasks.append({"idx": st_idx + 1,
                                        "testcases": public_testcases})
            ranking_details.append("%g" % round(st_score, 2))

        return score, subtasks, public_score, public_subtasks, ranking_details

    def get_public_outcome(self, outcome, unused_parameter):
        if outcome <= 0.0:
            return N_("Not correct")
        elif outcome >= 1.0:
            return N_("Correct")
        else:
            return N_("Partially correct")

    def reduce(self, outcomes, unused_parameter):
        return min(outcomes)
