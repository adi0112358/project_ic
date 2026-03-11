import { LabValues } from "./types";

const num = "([0-9]+(?:\\.[0-9]+)?)";

function findFirst(patterns: RegExp[], text: string): number | null {
  for (const pat of patterns) {
    const match = text.match(pat);
    if (match && match[1]) {
      const val = parseFloat(match[1]);
      if (!Number.isNaN(val)) return val;
    }
  }
  return null;
}

export function extractLabsFromText(text: string): LabValues {
  if (!text) return {};
  const cleaned = text.replace(/,/g, " ");

  const labs: LabValues = {
    age_years: findFirst([new RegExp(`age[^0-9]{0,10}${num}`, "i"), new RegExp(`${num}\\s*years`, "i")], cleaned),
    bmi: findFirst([new RegExp(`bmi[^0-9]{0,10}${num}`, "i")], cleaned),
    diabetes_duration_years: findFirst([new RegExp(`duration[^0-9]{0,10}${num}\\s*(years|yrs)`, "i")], cleaned),
    hba1c_percent: findFirst([new RegExp(`hba1c[^0-9]{0,10}${num}\\s*%?`, "i"), new RegExp(`a1c[^0-9]{0,10}${num}\\s*%?`, "i")], cleaned),
    fpg_mg_dl: findFirst([new RegExp(`(fpg|fasting plasma glucose|fasting glucose)[^0-9]{0,10}${num}`, "i")], cleaned),
    ogtt_2h_mg_dl: findFirst([new RegExp(`(ogtt|oral glucose)[^0-9]{0,10}${num}`, "i"), new RegExp(`2\\s*hr[^0-9]{0,10}${num}`, "i")], cleaned),
    crp_mg_l: findFirst([new RegExp(`crp[^0-9]{0,10}${num}`, "i"), new RegExp(`c\\s*-?\\s*reactive protein[^0-9]{0,10}${num}`, "i")], cleaned),
    neutrophils_abs: findFirst([new RegExp(`neutrophil[^0-9]{0,10}${num}`, "i")], cleaned),
    lymphocytes_abs: findFirst([new RegExp(`lymphocyte[^0-9]{0,10}${num}`, "i")], cleaned),
    nlr: findFirst([new RegExp(`nlr[^0-9]{0,10}${num}`, "i"), new RegExp(`neutrophil[^\\n]{0,20}lymphocyte[^0-9]{0,10}${num}`, "i")], cleaned),
    cd4_count: findFirst([new RegExp(`cd4[^0-9]{0,10}${num}`, "i")], cleaned),
    il6_pg_ml: findFirst([new RegExp(`il\\s*-?\\s*6[^0-9]{0,10}${num}`, "i")], cleaned),
    il17_pg_ml: findFirst([new RegExp(`il\\s*-?\\s*17[^0-9]{0,10}${num}`, "i")], cleaned),
    tnf_alpha_pg_ml: findFirst([new RegExp(`tnf\\s*-?\\s*alpha[^0-9]{0,10}${num}`, "i"), new RegExp(`tnf\\s*-?\\s*a[^0-9]{0,10}${num}`, "i")], cleaned),
    beta_hydroxybutyrate_mmol_l: findFirst([new RegExp(`beta\\s*-?\\s*hydroxybutyrate[^0-9]{0,10}${num}`, "i"), new RegExp(`b\\s*-?\\s*hba?[^0-9]{0,10}${num}`, "i")], cleaned),
    urine_albumin_mg_g: findFirst([new RegExp(`urine albumin[^0-9]{0,10}${num}`, "i"), new RegExp(`albumin[^0-9]{0,10}${num}\\s*(mg/g|mg\\s*/\\s*g)`, "i")], cleaned)
  };

  if (!labs.nlr && labs.neutrophils_abs && labs.lymphocytes_abs) {
    labs.nlr = Math.round((labs.neutrophils_abs / labs.lymphocytes_abs) * 1000) / 1000;
  }

  return labs;
}
