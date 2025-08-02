import { DoseTime } from './DoseTime.js';

export class Schedule {
  constructor({
    start_date,
    end_date,
    frequency,
    interval,
    day_of_month,
    doses_per_period,
    dose_amount,
    dose_unit,
    dose_times = [],
    days_of_week = []
  }) {
    this.start_date = start_date;
    this.end_date = end_date;
    this.frequency = frequency;
    this.interval = interval;
    this.day_of_month = day_of_month;
    this.doses_per_period = doses_per_period;
    this.dose_amount = dose_amount;
    this.dose_unit = dose_unit;
    this.dose_times = dose_times.map(dt => new DoseTime(dt.time, dt.dose_amount, dt.dose_unit));
    this.days_of_week = days_of_week;
  }
}
