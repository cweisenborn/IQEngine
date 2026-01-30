import Plot from 'react-plotly.js';
import React, { useEffect, useState } from 'react';
import { fftshift } from 'fftshift';
import { template } from '@/utils/plotlyTemplate';
import { FFT } from '@/utils/fft';
import { useSpectrogramContext } from '../hooks/use-spectrogram-context';

interface FreqPlotProps {
  displayedIQ: Float32Array;
  fftStepSize: Number;
}

export const FrequencyPlot = ({ displayedIQ, fftStepSize }: FreqPlotProps) => {
  const { spectrogramWidth, spectrogramHeight, meta, includeRfFreq } = useSpectrogramContext();
  const [frequencies, setFrequencies] = useState([]);
  const [magnitudes, setMagnitudes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Track if we currently have valid data loaded (prevents Plot rendering before/without data)
  // Note: This flag is reset to false when data becomes invalid or empty
  const hasEverHadData = React.useRef(false);
  
  const sampleRate = meta.getSampleRate();
  const centerFrequency = meta.getCenterFrequency();

  useEffect(() => {
    console.log('[FrequencyPlot] useEffect triggered', {
      hasDisplayedIQ: !!displayedIQ,
      displayedIQLength: displayedIQ?.length,
      fftStepSize: fftStepSize,
      isLoading,
      hasEverHadData: hasEverHadData.current,
    });

    if (displayedIQ && displayedIQ.length > 0) {
      // Check if displayedIQ contains valid data (not all -Infinity)
      // For performance, only check a sample of values
      const sampleSize = Math.min(100, displayedIQ.length);
      const hasValidData = Array.from(displayedIQ.slice(0, sampleSize)).some((val) => val !== -Infinity && !isNaN(val));
      
      console.log('[FrequencyPlot] Data validation', {
        sampleSize,
        hasValidData,
        firstFewValues: Array.from(displayedIQ.slice(0, 10)),
      });
      
      if (!hasValidData) {
        console.log('[FrequencyPlot] Invalid data detected, staying in loading state');
        setIsLoading(true);
        hasEverHadData.current = false; // Reset flag when data becomes invalid
        return;
      }

      console.log('[FrequencyPlot] Processing valid data...');
      // Calc PSD
      const fftSize = Math.pow(2, Math.floor(Math.log2(displayedIQ.length / 2))); // closest power of 2, rounded down
      const f = new FFT(fftSize);
      let out = f.createComplexArray(); // creates an empty array the length of fft.size*2
      f.transform(out, displayedIQ.slice(0, fftSize * 2)); // assumes input (2nd arg) is in form IQIQIQIQ and twice the length of fft.size
      out = out.map((x) => x / fftSize);
      let mags = new Array(out.length / 2);
      for (let j = 0; j < out.length / 2; j++) {
        mags[j] = Math.sqrt(Math.pow(out[j * 2], 2) + Math.pow(out[j * 2 + 1], 2)); // take magnitude
      }
      fftshift(mags); // in-place
      mags = mags.map((x) => 10.0 * Math.log10(x));
      setMagnitudes(mags);

      // calc x-axis
      const step = sampleRate / fftSize;
      const freqs = !includeRfFreq
        ? Array.from({ length: fftSize }, (_, i) => sampleRate / -2.0 + step * i)
        : Array.from({ length: fftSize }, (_, i) => sampleRate / -2.0 + step * i + centerFrequency);
      setFrequencies(freqs);
      
      console.log('[FrequencyPlot] Data processed successfully', {
        frequenciesLength: freqs.length,
        magnitudesLength: mags.length,
      });
      
      hasEverHadData.current = true; // Mark that we've successfully loaded data
      setIsLoading(false);
      console.log('[FrequencyPlot] State updated: isLoading=false, hasEverHadData=true');
    } else {
      console.log('[FrequencyPlot] No data or empty data, staying in loading state');
      setIsLoading(true);
      hasEverHadData.current = false; // Reset flag when no data
    }
  }, [displayedIQ, includeRfFreq, sampleRate, centerFrequency]); // TODO make sure this isnt going to be sluggish when currentSamples is huge

  return (
    <div className="px-3">
      <p className="text-primary text-center">
        Below shows the power spectral density of the sample range displayed on the spectrogram tab
      </p>
      {(() => {
        console.log('[FrequencyPlot] Render decision', {
          fftStepSize,
          isLoading,
          hasEverHadData: hasEverHadData.current,
          hasFrequencies: !!frequencies,
          frequenciesLength: frequencies?.length,
          hasMagnitudes: !!magnitudes,
          magnitudesLength: magnitudes?.length,
        });
        
        if (fftStepSize !== 0) {
          console.log('[FrequencyPlot] fftStepSize is not 0, showing message');
          return <p className="text-center text-sm">Plot only visible when Zoom Out Level is minimum (0)</p>;
        }
        
        const shouldRender = !isLoading && hasEverHadData.current && frequencies && magnitudes && frequencies.length > 0 && magnitudes.length > 0;
        console.log('[FrequencyPlot] Should render plot?', shouldRender);
        
        if (!shouldRender) {
          return <p className="text-center text-sm">Loading frequency data...</p>;
        }
        
        // Use scatter (SVG) instead of scattergl (WebGL) to avoid WebGL buffer issues
        // scattergl was causing "clear() called with no buffers" errors for certain data sizes
        const plotType = 'scatter';
        console.log('[FrequencyPlot] Using plot type:', plotType, 'for data length:', magnitudes.length);
        
        return (
          <Plot
            data={[
              {
                x: frequencies,
                y: magnitudes,
                type: plotType,
              },
            ]}
            layout={{
              width: spectrogramWidth,
              height: spectrogramHeight,
              margin: {
                l: 0,
                r: 0,
                b: 0,
                t: 0,
                pad: 0,
              },
              dragmode: 'pan',
              template: template,
              xaxis: {
                title: 'Frequency',
              },
              yaxis: {
                title: 'Magnitude',
                fixedrange: false,
              },
            }}
            config={{
              displayModeBar: true,
              scrollZoom: true,
            }}
          />
        );
      })()}
    </div>
  );
};
