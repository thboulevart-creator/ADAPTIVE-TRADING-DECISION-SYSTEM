# AP4 — handoff local
Date : 2026-09-25
Branche gouvernée : integration/system-v1.
Helper figé au commit cc329b3cbe55c24072d6382aee600a5509eb4609.
Path tools/ap4_price_structure.py.
SHA-256 f957b38a252ffb2649602fdc5405b82735c88300e1f32cc9fee5f41834098987.
Verdict helper PASS pour tentative locale ; AP4 corpus BLOCKED avant résultat.

Entrées attendues :
- %USERPROFILE%\Documents\ATDS-DERIVED\USTECH_PROFILE_MINUTE_CORE_V0_1
- AP0-MANIFEST.json dans cette racine
- %TEMP%\ATDS-AP3-EXPANSION-COMPRESSION.json, SHA-256 caa2d02942d5cbd05bcfadd0dedfabde000e4e941cdf4aa4b0433801f76f42ef.

Lire uniquement les fichiers AP0 existants et AP3.
Extraire le helper via git show depuis le commit figé, pas depuis une branche mouvante.
Vérifier son SHA-256 avant exécution.
Pas de changement de branche, pull, reset, installation, suppression ou écrasement de preuve.
Si output déjà présent : envoyer cet output et le terminal avant toute répétition.

Commande Python une fois le helper extrait :
python <helper> --ap0-root <racine> --ap0-manifest <racine>/AP0-MANIFEST.json --ap3-report <TEMP>/ATDS-AP3-EXPANSION-COMPRESSION.json

Résultat attendu :
AP4_COMPLETE
puis ATDS-AP4-PRICE-STRUCTURE.json dans TEMP.
Joindre JSON exact et terminal. En cas de BLOCKED_AP4, envoyer terminal ; aucun rapport n'est écrasé.
Après réception : fresh HEAD, SHA-256, adjudication AP4, observations qualifiées, puis AP5 seulement si PASS.
