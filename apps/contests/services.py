from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, ValidationError as DjangoValidationError
from django.http.response import HttpResponseServerError

from .general_selectors import (
    current_contest_retrieve,
    retrieve_current_scramble
)
from .models import (
    RoundSessionModel,
    SolveModel,
    ContestModel,
    DisciplineModel,
    ScrambleModel,
)
from scripts.cube import ReconstructionValidator

User = get_user_model()


class CreateSolveService:
    def __init__(self, user_id, discipline_slug):
        self.user = User.objects.get(id=user_id)
        try:
            self.discipline = DisciplineModel.objects.get(slug=discipline_slug)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist
        self.contest = current_contest_retrieve()
        if not self.round_session_is_finished():
            pass
        else:
            raise PermissionDenied
        self.current_scramble = self.retrieve_current_scramble()
        self.round_session = self.retrieve_current_round_session()

    def create_solve(self, scramble_id, reconstruction, is_dnf, time_ms):
        """
        - check for authorization details (or raise 401) +
        - check if user can solve contest (or raise 403) +
        - find current contest (or raise 404 or 500 (need to decide)) +
        - check if this solve is for right scramble (or raise 400) +
        - validate solve moves correctness (if not save as dnf and send TODO something)
        - save solve +
        - save solve to round_session (mb as an atomic transaction with 4.)
        - return solve
        """
        # validate scramble
        if self.scramble_is_correct(scramble_id=scramble_id):
            pass
        else:
            raise DjangoValidationError
        # validate that scramble wasn't solved yes
        if self.solve_does_not_exists():
            pass
        else:
            raise PermissionDenied('solve already exists')
        # validate solve reconstruction
        solve_is_valid = self.solve_is_valid(
            reconstruction=reconstruction,
            time_ms=time_ms
        )
        if solve_is_valid:
            pass
        else:
            is_dnf = True

        solve = SolveModel.objects.create(
            time_ms=time_ms,
            is_dnf=is_dnf,
            reconstruction=reconstruction,
            submission_state='pending',

            user=self.user,
            contest=self.contest,
            discipline=self.discipline,
            round_session=self.round_session,
            scramble=self.current_scramble,
        )
        # TODO add solve to current_round_session
        return solve

    def round_session_is_finished(self):
        try:
            round_session = RoundSessionModel.objects.get(
                contest=self.contest,
                discipline=self.discipline,
                user=self.user,
            )
            return round_session.is_finished
        except ObjectDoesNotExist:
            return False

    def retrieve_current_scramble(self):
        current_scramble = retrieve_current_scramble(
            user=self.user,
            contest=self.contest
        )
        return current_scramble

    def scramble_is_correct(self, scramble_id):
        try:
            scramble = ScrambleModel.objects.get(id=scramble_id)
        except ObjectDoesNotExist:
            raise DjangoValidationError
        if scramble == self.current_scramble:
            return True
        else:
            return False

    def solve_is_valid(self, reconstruction, time_ms):
        reconstruction_validator = ReconstructionValidator(
            scramble=self.current_scramble.moves,
            reconstruction=reconstruction,
        )
        if reconstruction_validator.is_valid():
            return True
        else:
            return False

    def solve_does_not_exists(self):
        try:
            solve = self.contest.solve_set.get(
                discipline=self.discipline,
                user=self.user,
                scramble=self.current_scramble,
            )
            return False
        except ObjectDoesNotExist:
            return True

    def create_round_session(self):
        round_session = RoundSessionModel.objects.create(
                contest=self.contest,
                discipline=self.discipline,
                user=self.user,
            )
        return round_session

    def retrieve_current_round_session(self):
        try:
            round_session = RoundSessionModel.objects.get(
                contest=self.contest,
                discipline=self.discipline,
                user=self.user,
            )
            return round_session
        except ObjectDoesNotExist:
            round_session = self.create_round_session()
            return round_session


class RoundSessionService:
    def round_session_create(self, contest_id, discipline_id, user_id):
        contest = ContestModel.objects.get(id=contest_id)
        discipline = DisciplineModel.objects.get(id=discipline_id)
        user = User.objects.get(id=user_id)
        round_session = RoundSessionModel(contest=contest, discipline=discipline, user=user)
        round_session.save()
        return round_session

    def round_session_finish(self):
        pass
