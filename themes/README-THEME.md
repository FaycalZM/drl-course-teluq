# Thème hugo-book — version vendorisée et épinglée

**Révision : `be741b014820077e76cf60250f55574408161059`** (tag `v13-7-gbe741b0`, 2026-03-15)
— exactement celle du cours LLM, donc connue compatible avec **Hugo 0.157.0**.

## Pourquoi vendorisé et non en sous-module

1. `git submodule add` échoue sur ce dossier monté (écriture impossible dans
   `.git/modules/`). Les fichiers sont donc suivis normalement par git.
2. Le `main` du thème **ne compile pas** avec Hugo 0.157 : il utilise
   `.Site.Language.Locale`, qui n'existe pas encore dans cette version
   (`can't evaluate field Locale in type *langs.Language`). Épingler est donc
   nécessaire, pas seulement préférable.

Avantage collatéral : plus d'étape `git submodule update --init` à oublier, en local comme
dans la CI.

## Mettre à jour le thème, plus tard

```bash
cd drl-course
rm -rf themes/hugo-book
git clone https://github.com/alex-shpak/hugo-book themes/hugo-book
cd themes/hugo-book && git checkout <nouvelle-révision> && cd ../..
rm -rf themes/hugo-book/.git
hugo --minify          # doit sortir en code 0 AVANT de committer
```

Toute mise à jour exige de rebâtir et de vérifier : le thème et la version de Hugo sont
couplés. **Ne jamais modifier les fichiers de `themes/`** — les surcharges vont dans
`drl-course/layouts/`.

## Si tu préfères un sous-module (sous Windows, git natif)

```powershell
rmdir /s /q drl-course\themes\hugo-book
cd drl-course
git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
cd themes\hugo-book ; git checkout be741b014820077e76cf60250f55574408161059
```
