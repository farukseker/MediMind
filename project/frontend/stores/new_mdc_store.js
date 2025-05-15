import { defineStore } from 'pinia';

export const useNewMdcStore = defineStore('new_mdc_store', {
  state: () => ({
    medicine_name: '',
    medicine_notes: '',
    start_date: '',
    end_date: '',
    // temp values
    // DoseTime-START
    dose_times:[],
    // DoseTime-END 
    // Schedule-START
    dose_amount: 1,
    dose_unit: 'miligram',
    frequency: '', // (daily | weekly | monthly | custom)
    days_of_week: [],
    day_of_month: 1,
    interval: 1,
    // Schedule-END
    form_index: 0,
    dose_unit_list: [
    {
        param: "ui",
        value:"UI"
    },
    {
        param: "microgram",
        value:"MCG"
    },
    {
        param: "miligram",
        value:"MG"
    },
    {
        param: "gram",
        value:"GR"
    },
    {
        param: "mililitre",
        value:"ML"
    },
    {
        param: "pieces",
        value:"Tane"
    },
    {
        param: "amp",
        value:"Ampül"
    },
    {
        param: "drop",
        value:"Damla"
    }
]
  }),
  actions: {

  },
});

