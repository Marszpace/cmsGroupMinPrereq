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


class GroupMinPrereqDisplay(ScoreTypeGroup):
    """The score of a submission is the sum of the product of the
    minimum of the score of each testcases within a range, as well
    as their prerequisites, with the multiplier within each range.

    In particaluar, it should function as if we put every testcase 
    from prerequisites into a subtask/group/range.

    Parameters are [[m, t, [p1, p2, ..., pi]], ... ]. prerequisite 
    are *one-based* indexed.
    """

    def retrieve_target_testcases(self):
        """Return the list of the target testcases for each subtask.

        Each element of the list consist of multiple strings.
        Each string represents the testcase name which should be included
        to the corresponding subtask.
        The order of the list is the same as 'parameters'.

        return ([[unicode]]): the list of the target testcases for each task.

        """

        t_params = [p[1] for p in self.parameters]

        if all(isinstance(t, int) for t in t_params):

            # XXX Lexicographical order by codename
            indices = sorted(self.public_testcases.keys())
            current = 0
            targets = []

            for t in t_params:
                next_ = current + t
                targets.append(indices[current:next_])
                current = next_

            return targets

        elif all(isinstance(t, str) for t in t_params):

            indices = sorted(self.public_testcases.keys())
            targets = []

            for t in t_params:
                regexp = re.compile(t)
                target = [tc for tc in indices if regexp.match(tc)]
                if not target:
                    raise ValueError(
                        "No testcase matches against the regexp '%s'" % t)
                targets.append(target)


        else:
            raise ValueError(
                "In the score type parameters, the second value of each element "
                "must have the same type (int or unicode)")
            
        """
        This part assumes that the given parameters are valid (the admin is 
        responsible for asserting this), and that for each subtask, its
        prerequisite are strictly before it, i.e. that 1...n is a valid 
        grading sequence.
        """
        for target, parameter in enumerate(self.parameters):
            for pr_idx in parameter[2]:
                targets[target] += targets[pr_idx-1]

        return targets


    def get_public_outcome(self, outcome, unused_parameter):
        if outcome <= 0.0:
            return N_("Not correct")
        elif outcome >= 1.0:
            return N_("Correct")
        else:
            return N_("Partially correct")

    def reduce(self, outcomes, unused_parameter):
        return min(outcomes)

