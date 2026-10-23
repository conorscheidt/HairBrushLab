
## Presentation Script - Group 4

**Vivian, 0:00-0:32** (force-time graphs/traces)

Mr. Shada, we used 15 of our 16 files and took the peak load as each brush's strength. In file 5 the load flattens near 199 pounds, and the video shows the brush twisting in the fixture but staying in one piece, so that peak isn't actually a joint failure. File 6 retests the same brush, so we counted it once. We kept brush 2 at 107. Even though it's below spec, it's still a valid failure.

**Mosawer, 0:32-1:04** (assumptions)

There's no trend with test order and no outliers in the box plot. The normal plot is close to a line except for a mild gap between 159 and 199, so assuming normality is pretty reasonable. E1, the mean minus 1.28 standard deviations, is 124.6 pounds. E2, the sample tenth percentile, is 127. They agree within three pounds.

**Victor, 1:04-1:42** (distributions/interval plot)

We simulated 10,000 samples of 15 from that normal fit. Both estimators come out less than two pounds high, but E1 is tighter: a standard deviation of 16.1 against 19.4, and 31 percent lower MSE (mean squared error). So we chose E1. E1 plus or minus 1.96 times 16.1 gives 93 to 156 pounds, which contains 110. With all 16 files it's 97 to 157, so dropping file five doesn't actually change that.

**Conor, 1:42-2:30** (interval plot)

Ms. Lytle, we recommend paying for more testing. Fourteen of fifteen brushes held 110 pounds, and our best estimate is that around 5 percent would fail, under the 10 percent limit. But only fifteen brushes doesn't rule out a failure rate close to one in five. Leaving the process as it is risks warranty issues, and strengthening the handles adds cost to every brush for a problem we might not actually have. We'd test about 130 more brushes from several production runs. If the process is as good as it seems here, that gives about an 80 percent chance of a clear answer. If the range then sits above 110, we should leave the process alone. If it sits below, we should strengthen the handles.