import readline from "readline";
import type { IFTestPromptProcesser } from "./common/interface";
import type { DeviationSpamAnalysisResult, MessageTimestampElement } from "./common/type";
import { DeviationBaseSpammmingDetector } from "./deviation_base_spamming_detector";


export class TestPromptProcesser implements IFTestPromptProcesser {
    collectionSize: number = NaN;
    readline!: readline.Interface;
    SpamDetector!: DeviationBaseSpammmingDetector

    constructor(collectCount: number = 0) {
        this.readline = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
        });
        this.collectionSize = collectCount
        this.SpamDetector = new DeviationBaseSpammmingDetector()
    }

    setMainSection(i: number): void {
        this.readline.question(`message [ ${i} ]\t`, answer => {
            let millisecond = new Date().getTime()
            this.SpamDetector.collectTimestamp(millisecond)
            if (this.SpamDetector.timestampQueue.size >= 4) {
                const result = this.SpamDetector.getRepetitionScoreArray()
                return this.displaySection(result)
            } else {
                return this.setMainSection(i++);
            }
        });
    }

    displaySection({ messageTimestamps, delays, repetitionScores, epsilon, timeoutLimit }: DeviationSpamAnalysisResult): void {
        let totla_score = 1
        let question = `[ analysis result ]\n`
        question += `1. message timestamp\n`
        for(let i=0; i < messageTimestamps.length; i++) {
            question += `\t(${i}). ${messageTimestamps[i]}\n`
        }

        question += `2. delay\n`
        for(let i=0; i < delays.length; i++) {
            question += `\t(${i}). ${delays[i]}\n`
        }

        question += `3. repetitionScores\n`
        for(let i=0; i < repetitionScores.length; i++) {
            question += `\t(${i}). ${repetitionScores[i]}\n`
            totla_score *= repetitionScores[i]
        }

        question += `4. total repetitionScores\n`
        question += `\t(${0}). ${totla_score}\n`

        question += 'press the Enter . . .'

        this.readline.question(question, answer => {
            return this.setMainSection(1)
        })
    }

}