import * as fs from 'fs';

(() => {
    type Report = number[];
    type Reports = Report[];
    type Results = {
        safeCt: number;
        safeCtWithDampener: number;
    };

    const readInput = (filename: string): Reports =>
        fs.readFileSync(filename, 'utf8')
            .trim()
            .split(/\r?\n/)
            .map(line => line.split(/\s+/).map(Number));

    const isSafe = (report: Report): boolean => {
        const deltas = report.slice(1).map((value, i) => value - report[i]);
        const normalizedDeltas = deltas[0] < 0 ? deltas.map(d => -d) : deltas;
        return normalizedDeltas.every(d => d >= 1 && d <= 3);
    };

    const solve = (reports: Reports): Results => {
        let safeCt = 0;
        let safeCtWithDampener = 0;

        for (const report of reports) {
            if (isSafe(report)) {
                safeCt++;
            } else {
                for (let i = 0; i < report.length; i++) {
                    const dampenedReport = [...report.slice(0, i), ...report.slice(i + 1)];
                    if (isSafe(dampenedReport)) {
                        safeCtWithDampener++;
                        break;
                    }
                }
            }
        }

        return { safeCt: safeCt, safeCtWithDampener: safeCt + safeCtWithDampener };
    };

    const main = () => {
        const filename = process.argv[2] || 'input.txt';
        const reports = readInput(filename);
        const { safeCt, safeCtWithDampener } = solve(reports);

        console.log("Part 1: safe_ct =", safeCt);
        console.log("Part 2: safe_ct_with_dampener =", safeCtWithDampener);
    };

    main();
})();
