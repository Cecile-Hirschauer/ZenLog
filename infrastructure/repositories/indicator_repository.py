from domain.entities.indicator import Indicator
from domain.ports.indicator_repository import IndicatorRepository
from infrastructure.models import Indicator as IndicatorModel


class DjangoIndicatorRepository(IndicatorRepository):
    """Django ORM adapter for IndicatorRepository."""

    def find_by_id(self, indicator_id: str) -> Indicator | None:
        try:
            model = IndicatorModel.objects.get(id=indicator_id)
            return self._to_entity(model)
        except IndicatorModel.DoesNotExist:
            return None

    def find_all_active(self) -> list[Indicator]:
        qs = IndicatorModel.objects.filter(is_active=True)
        return [self._to_entity(model) for model in qs]

    def save(self, indicator: Indicator) -> Indicator:
        model, created = IndicatorModel.objects.update_or_create(
            id=indicator.id,
            defaults={
                "name": indicator.name,
                "unit": indicator.unit,
                "min_value": indicator.min_value,
                "max_value": indicator.max_value,
                "is_active": indicator.is_active,
            },
        )
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: IndicatorModel) -> Indicator:
        return Indicator(
            id=str(model.id),
            name=model.name,
            unit=model.unit,
            min_value=model.min_value,
            max_value=model.max_value,
            is_active=model.is_active,
        )
