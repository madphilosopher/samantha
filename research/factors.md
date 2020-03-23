# Several Factors

    From: https://security.stackexchange.com/questions/47475/testing-a-hardware-random-number-generator
    User: https://security.stackexchange.com/users/5400/polynomial
    Date: 2020-03-22

There are several factors at play here:

1. The physical HRNG mechanism used inside the ARM microprocessor.
2. The supporting logic on the silicon inside the microprocessor.
3. The microcode deployed on the microprocessor.
4. The implementation of the RNG inside Linux.

According to the manufacturer, that particular chip uses noise from
a reverse bias transistor, in an open-collector HRNG design. This is
precisely the hardware I'm using in my current HRNG project, but much
smaller. It's one of the cheapest ways to implement a HRNG directly into
silicon; whereas I'm using discrete transistors, the ARM processor simply
shrinks this to a few blips of silicon on the chip die.

We know that this mechanism is a strong source of randomness, because
it relies upon a phenomenon called quantum tunnelling, which is known
to be probabilistic and random. The basic idea is that electrons will
randomly "jump" over the band gap inside the transistor, leading to
a randomly fluctuating signal. We can then amplify this (simple PNP
transistor amplifier will do) and interpret the output as either a 1
or a 0 by sampling the result at a fixed frequency - if it exceeds a
certain threshold it's a 1, otherwise it's a 0.

One slight deficiency of this mechanism is that any DC leakage will lead
to a skew towards 1s appearing more often than 0s. In order to get around
this, we can use a simple trick called von Neumann decorrelation, which
essentially involves encoding bit pairs 01 and 10 to 0 and 1 respectively,
and ignoring all 00 and 11 pairs. This produces a statistically unbiased
stream.

I can almost certainly guarantee that this is the mechanism by which
it produces random numbers. There's one major alternative (two reverse
biased NOT gates in parallel) but it's covered by an Intel patent,
so I doubt ARM is using that. Unfortunately, the only way to know for
certain is to grab some acid and decap a chip, then take a microscope
and start reverse engineering the silicon. I don't happen to have the
spare gear available for this.

The potential vulnerability that you might find in such exploration is
that high frequency clock signals or other HF data lines are routed very
close to the HRNG or its supporting logic, leading to a potential for
interference. This is usually unlikely in ICs, but we're talking about
high sensitivity applications here, so it's worth looking for. Even if
it were the case, though, I don't see it providing a useful skew from
a cryptanalytic perspective.

The next potential for exploitation is microcode. Recently, a researcher
demonstrated that it was possible to patch microcode for Intel processors
to look for unique patterns in the instruction buffer and detect when the
RDRAND instruction was being used to fill the `/dev/random` pool. It would
then identify the position of that pool buffer in the processor cache
and effectively zero it, causing the zero pool to be copied back into
system memory. This meant that `/dev/random` would constantly output the
same attacker-controlled value, with obviously devastating results. If
a similar but more subtle trick was employed in the ARM microcode, it
might be possible to massively reduce the entropy of the HRNG in a way
that is only known to the creator of the patch. Detecting such tricks
would be difficult, but it could be done by extracting the microcode
and analysing it.

Finally, the last problem is the RNG design inside the Linux kernel. The
`/dev/random` pool is usually fed from a bunch of state-based sources, using
a mixing algorithm that is built upon a cryptographic function. However,
when RDRAND or similar instructions are available, the engine simply
XORs the data over the pool. This isn't exactly a good idea, because
it makes it easy to screw with the pool data in a meaningful way by
producing certain values. If the stronger mixing function were used,
the attacker would need to break that (or do something more conspicuous)
in order to gain meaningful control over the pool.

There is not an obvious answer to your question. Hardware random number
generators can be very high quality, but it's difficult to analyse their
implementation given only a consumer device. That being said, if you're
going to distrust your hardware, you can't really make any guarantees
in the first place. If you want to limit the scope of distrust entirely
to the quality of random numbers produced, then design your supporting
system around that fact.

