/-! Synthetic negative fixtures A–E. Intentionally includes `sorry` and an extra axiom. -/
namespace CrosswalkProbe
namespace Basic
-- A: direct sorry
 theorem thm_direct_gap : False := by sorry
-- B: transitive sorry
 theorem helper_gap : False := by sorry
 theorem thm_transitive_gap : False := helper_gap
-- C: fully closed
 theorem thm_closed_formal : True := by trivial
-- D: custom axiom, no sorry
 axiom externalAssumption : False
 theorem thm_custom_axiom : False := externalAssumption
-- E: both transitive sorry and custom axiom
 theorem thm_mixed : False ∧ False := And.intro helper_gap externalAssumption
end Basic
end CrosswalkProbe
