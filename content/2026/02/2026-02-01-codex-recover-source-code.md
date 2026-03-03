---
title: "How I Used Codex to \\\"Recover\\\" Lost Source Code in 5 Days"
date: 2026-02-01
original_url: https://baoyu.io/blog/2026/01/31/codex-recover-source-code
---

[See all posts](/translations)

Published on 2026-02-01

# How I Used Codex to \"Recover\" Lost Source Code in 5 Days

作者：

宝玉

![How I Used Codex to \"Recover\" Lost Source Code in 5 Days](https://s.baoyu.io/imgs/2026-01-31/codex-recover-source-code/cover.png)

Ever lost your source code? It's a terrible feeling. Years ago, I built an Electron drawing app. Then I lost the source code. All I had left was the compiled version.

I thought about rewriting it from scratch, but the idea of recreating all those little details felt overwhelming. Then I read OpenAI's blog post about building the Sora Android app in 28 days with Codex, and I had an idea: the compiled code was still there. **Could I get Codex to reverse-engineer it back into source code?**

Five days later, I had working TypeScript source code. Here's how it happened.

## 1. Extracting Module Structure from Obfuscated Code

Electron apps bundle everything into an `asar` file. Step one was getting Codex to extract the JS and CSS files from it.

The extracted JavaScript was compiled and obfuscated. Variable names like `a`, `b`, `c`. Function calls tangled into unreadable chains. A human would get dizzy looking at it. But for Codex, it was just another piece of code to analyze.

I asked Codex to analyze the main JS files and list out the modules. It actually did it. The original module names were gone, but from the code structure and logic patterns, **Codex reconstructed a fairly complete module inventory**.

With that inventory, I had Codex create a restoration plan: convert each module from obfuscated JavaScript back into readable TypeScript. The module list became a checklist. Every completed module got a checkmark.

![From obfuscated code to organized module inventory](https://s.baoyu.io/imgs/2026-01-31/codex-recover-source-code/01-infographic-module-extraction.png)

## 2. First Problem: Codex Wanted to “Prove” the Code Worked

Early in the restoration process, I hit a snag.

Codex has this instinct: it really wants to verify that generated code actually runs. To make the code build successfully, it would quietly skip parts it deemed “not immediately necessary.”

For writing new code, that's a good habit. For restoring old code, it's a disaster. **I needed complete restoration, not a minimal subset that compiles.**

The fix was simple. I added a strict rule to `AGENT.md`:

> “Restore modules one by one. Do not worry about making the code compile.”

That single line changed everything. Codex stopped obsessing over build errors and started faithfully restoring module by module.

## 3. Second Problem: Context Fills Up, Memory Disappears

Codex has a limited context window. Back then, it would stop after running for a while, and I'd have to keep typing “continue.” If I started a new session, I'd have to explain the whole task again.

**The problem:** a new Codex session doesn't know what happened before. You have to re-explain the entire background.

My solution was to build an **“external memory” system**:

- Describe the overall task background in `AGENT.md`
- Create a `PLAN.md` file to track the restoration plan and current progress
- Add a rule to `AGENT.md`: always read `PLAN.md` first, and update `PLAN.md` after each work session

This way, every new session just needed “continue” as input. Codex would automatically read the progress file and pick up where it left off.

Eventually, I got tired of even doing that manually. I had Codex write a script that detected when context was getting full, automatically started a new session, and typed “continue.”

So I just watched it run. Check back every now and then, and a few more modules were done.

![External memory system with AGENT.md and PLAN.md](https://s.baoyu.io/imgs/2026-01-31/codex-recover-source-code/02-infographic-external-memory.png)

## 4. Assembling the Pieces into a Working App

A few days later, all modules had been restored to TypeScript files. But these were still scattered parts.

Next step: assemble them into an actual working Electron app. I had Codex create a new project using Electron Forge scaffolding, then drop the restored code in.

At this point, I rewrote `AGENT.md` and `PLAN.md` to explain how to compile and test. Then the same routine: automatic new sessions, continue, update `PLAN`.

**What happened next was almost magical.**

I watched Codex continuously fix compilation errors. It would check the original compiled code to verify logic, run `npm start` to test the app, find problems, fix them, move on.

Once the modules mostly compiled, I worked with Codex to write integration tests covering the main user flows. After the tests were ready, it was the same loop: let Codex generate code, run tests, fix issues.

![Auto-fix loop: compile, test, find bugs, fix](https://s.baoyu.io/imgs/2026-01-31/codex-recover-source-code/03-infographic-auto-fix-loop.png)

## 5. Five Days Later

By the end of day five, I had an Electron app with complete source code that actually ran.

“Perfect restoration” would be an overstatement. There were still some runtime bugs. Some edge-case features behaved slightly differently than before. But the main functionality was there, the structure was clean, and most importantly, **I could finally modify the code again**.

## 6. What I Learned

A lot of people say Codex doesn't need an external loop mechanism. I think that's wrong.

**For long-running tasks, Codex needs something like a ralph-loop plugin.** Otherwise, you end up like me, writing your own script to periodically start new sessions and type “continue.” This should be a built-in feature.

A few other lessons:

**Plan and checklist are critical for long tasks.** You must update progress after each work session. If context breaks and progress isn't saved, previous work is wasted.

**Giving Codex a way to verify is equally important.** The only reason it could auto-fix bugs was because it could run `npm start` to see results and run tests to check correctness. Without verification, Codex can only write blind.

**Sometimes you need to tell Codex what NOT to do.** That rule about not worrying about compilation freed Codex to focus on what actually mattered.

---

OpenAI's blog post was about using Codex to build a production app from scratch in 28 days. My story is the opposite: using Codex to reverse-engineer a lost codebase back into source code in 5 days.

Different directions, but the same core methodology: treat Codex as a highly capable teammate who needs clear instructions, build an external memory system to maintain continuity, and provide verification methods so it can self-correct.

![Three pillars of Codex methodology: clear instructions, external memory, verification](https://s.baoyu.io/imgs/2026-01-31/codex-recover-source-code/04-infographic-methodology.png)

---

[See all posts](/translations)