import type { DeviationSpamAnalysisResult } from "./common/type";
import { DeviationBaseSpammmingDetector } from "./deviation_base_spamming_detector";
const MEDIAN_RANGE = 1


function testFunction(
    size: number = 100,
    time_deviation: number = 1000,
    limit_percentage: number = 80
) {
    // const timestampDataset = number();
    const spammingDetector = new DeviationBaseSpammmingDetector()
    const totalScores = Array<DeviationSpamAnalysisResult>()

    for (let i = 0; i < size; i++) {
        let time = 0
        for(let j = 0; j < 4; j++) {
            time += Math.floor(Math.random() * time_deviation ) + 1000
            spammingDetector.collectTimestamp(time)
        }
        const result = spammingDetector.getAnalysisResult()
        analysisDisplay(result)
        totalScores.push(result)
    }
    
    // TotalAnalysisDisplay(totalScores);
}

function calculateConditionalP(base: number, target: number) {
    
}

function generateDistribution(analysisResult: Array<DeviationSpamAnalysisResult>) {
    for (let i = 0; i < analysisResult.length; i++) {
        const isOverHalf = analysisResult[i].score_1.filter((x) => x > 0.5)
        if(isOverHalf.length == 0) {
            continue
        }

        // const conditionalP = 
    }
}

function findMedian(medianMap: Map<number, number>, analysisResult: Array<DeviationSpamAnalysisResult>) {
    for (let i = 0; i < analysisResult.length; i++) {
        const key = Math.floor(analysisResult[i].score_2*100 / MEDIAN_RANGE) * MEDIAN_RANGE

        if(!medianMap.has(key)) {
            medianMap.set(key, 0)
        }
        let value = medianMap.get(key)

        if(!value) {
            value = 0
        }
        value += 1

        medianMap.set(key, value)
    }

    let median: [number, number] =  [0, 0]
    for(const entry of medianMap.entries()) {
        if(median[1] < entry[1]) {
            median = entry
        }
    }
    return median[0]
}

function TotalAnalysisDisplay(analysisResult: Array<DeviationSpamAnalysisResult>) {
    let deviation:number = 0
    let mean: number = 0
    let medianMap: Map<number, number> = new Map<number, number>()
    let median_range = 0
    let maximum: number = 0

    let minimum: number = analysisResult[0]["score_2"]
    for (let i = 0; i < analysisResult.length; i++) {
        const totalScore = analysisResult[i].score_2
        if(maximum < totalScore) {
            maximum = totalScore
        }
        if(minimum > totalScore) {
            minimum = totalScore
        }

        mean += totalScore;
    }
    mean = mean / analysisResult.length
    median_range = findMedian(medianMap, analysisResult) 

    for (let i = 0; i < analysisResult.length; i++) {
        const totalScore = analysisResult[i].score_2
        deviation += (totalScore - mean)**2
    }
    deviation = Math.sqrt(deviation / analysisResult.length)

    let text = `[ total analysis ]\n`
    text += `1. statitics\n`
    text += `\t mean: ${(mean*100).toFixed(2)}\n`
    text += `\t median: ${median_range} ~ ${median_range+10}\n`
    text += `\t deviation: ${(deviation*100).toFixed(2)}\n`
    text += `\t maximum: ${(maximum*100).toFixed(2)}\n`
    text += `\t minimum: ${(minimum*100).toFixed(2)}\n`

    text += `[ distribution ]\n`
    
    for (let i = 0; i < medianMap.size; i++) {
        if(i*MEDIAN_RANGE == 100) {
            text += `${i*MEDIAN_RANGE}\t${medianMap.get(i*MEDIAN_RANGE)}\n`
        } else {
            
            text += `${i*MEDIAN_RANGE}-${(i+1)*MEDIAN_RANGE}\t${medianMap.get(i*MEDIAN_RANGE)}\n`
        }

    }


    // for (let i = 0; i < medianMap.size; i++) {
    //     if(i*10 == 100) {
    //         text += `\t range ${i*10}  count ${medianMap.get(i*10)}\n`
    //     } else {
    //     text += `\t range ${i*10}-${(i+1)*10}  count ${medianMap.get(i*10)}\n`
    //     }


    // text += `[ analysis data over 90% ]\n`
    // }
    // for (let i = 0; i < analysisResult.length; i++) {
    //     if(analysisResult[i].totalScore > 0.9) {
    //     text += `\t ${i}. [`
    //     for (let j = 0; j < analysisResult[i].delays.length; j++) {
    //         text += ` ${analysisResult[i].delays[j]} `
    //     }
    //     text += `]\n`
    //     }
    // }

    console.log(text)
}

function analysisDisplay({ messageTimestamps, delays, score_1: repetitionScores, epsilon, timeoutLimit }: DeviationSpamAnalysisResult) {
    let totla_score = 1
    let question = `[ analysis result ]\n`
    question += `1. message timestamp\n`
    for (let i = 0; i < messageTimestamps.length; i++) {
        question += `\t(${i}). ${messageTimestamps[i]}\n`
    }

    question += `2. delay\n`
    for (let i = 0; i < delays.length; i++) {
        question += `\t(${i}). ${delays[i]}\n`
    }

    question += `3. repetitionScores\n`
    for (let i = 0; i < repetitionScores.length; i++) {
        question += `\t(${i}). ${repetitionScores[i]}\n`
        totla_score *= repetitionScores[i]
    }

    question += `4. total repetitionScores\n`
    question += `\t(${0}). ${totla_score}\n`

    question += 'press the Enter . . .'

    console.log(question)
}

testFunction(1, 5000, )

// for (let i = 0; i < 5; i++) {
//     console.log(Math.random()*5000)
// }