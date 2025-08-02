import { Schedule } from './Schedule.js';

export class MedicationPayload {
  constructor({
    id,
    name,
    is_active,
    default_dose_amount,
    default_dose_unit,
    schedules = []
  }) {
    this.id = id;
    this.name = name;
    this.is_active = is_active;
    this.default_dose_amount = default_dose_amount;
    this.default_dose_unit = default_dose_unit;
    this.schedules = schedules.map(s => new Schedule(s));
  }
}
