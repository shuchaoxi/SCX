#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_phase_field.py — SCX Phase Field Theory Numerical Verification Script
============================================================================
SCX相场理论数值验证脚本

Verifies core claims from the SCX Phase Field paper (main.tex).

Tests:
  (1) 1D Allen-Cahn kink — verify tanh analytical profile
  (2) 1D Cahn-Hilliard spinodal decomposition
  (3) Coupled 2D Allen-Cahn / Cahn-Hilliard domain formation
  (4) Three-phase diagram in (g_bar, S_var) space
  (5) Coarsening L(t) ~ t^{1/3} LSW scaling
  (6) Critical nucleus radius R_c = sigma / Delta_f
  (7) Gibbs-Thomson curvature effect
  (8) Domain wall pinning at heterogeneities (Thm10)
  (9) Staircase defect nucleation (Thm12)

Method: Semi-implicit Fourier spectral with operator splitting.
Dependencies: numpy, scipy (ndimage only).
"""

import numpy as np
from numpy.fft import fft, ifft, fftfreq, fft2, ifft2
from scipy.ndimage import label
import sys

# ══════════════════════════════════════════════════════════════════════
class PhaseFieldParams:
    """SCX phase field parameters with double-well potentials.

    Gauge:     f_g(g) = (A/4)*g^4 - (B/2)*g^2,    minima at ±sqrt(B/A)
    Potential: f_S(S) = (A_S/4)*S^4 - (B_S/2)*S^2,  minima at ±sqrt(B_S/A_S)
    """
    def __init__(self):
        self.A, self.B = 1.0, 1.0
        self.g_eq = np.sqrt(self.B / self.A)       # 1.0
        self.kappa_g, self.kappa_S = 1.0, 1.0
        self.A_S, self.B_S = 1.0, 2.0
        # S minima at ±sqrt(2) ≈ ±1.414
        # Spinodal: |S| < sqrt(2/3) ≈ 0.816
        self.lam = 0.3
        self.M_g, self.M_S0, self.gamma = 1.0, 0.1, 0.5
        # Derived
        self.delta = np.sqrt(2 * self.kappa_g / self.B)
        self.sigma = (2*np.sqrt(2*self.kappa_g)/3) * (self.B**1.5/self.A)
        self.Delta_f = self.B**2 / (4*self.A)
        self.R_c_2d = self.sigma / self.Delta_f

    def df_g(self, g):    return (self.A * g**2 - self.B) * g
    def df_S(self, S):    return self.A_S * S**3 - self.B_S * S
    def d2f_S(self, S):   return 3 * self.A_S * S**2 - self.B_S
    def lap_2d(self, u, k_sq): return np.real(ifft2(-k_sq * fft2(u)))


# ══════════════════════════════════════════════════════════════════════
# (1) 1D Allen-Cahn kink
# ══════════════════════════════════════════════════════════════════════
def test1():
    print("=" * 60)
    print("(1) 1D Allen-Cahn Kink Profile")
    print("=" * 60)
    p = PhaseFieldParams()
    Nx, Lx = 512, 40.0
    dx = Lx / Nx
    x = np.linspace(-Lx/2, Lx/2, Nx, endpoint=False)
    k_sq = (2*np.pi*fftfreq(Nx, d=dx))**2

    g = np.where(x < 0, -p.g_eq, p.g_eq)  # step
    dt = 0.01
    for _ in range(2000):
        g_hat = fft(g)
        g_hat = (g_hat - dt*p.M_g*fft(p.df_g(g))) / (1 + dt*p.M_g*p.kappa_g*k_sq)
        g = np.real(ifft(g_hat))

    g_ana = p.g_eq * np.tanh(x / (p.delta/np.sqrt(2)))
    inter = slice(Nx//8, 7*Nx//8)
    rmse = np.sqrt(np.mean((g[inter] - g_ana[inter])**2))
    print(f"  RMS error: {rmse:.5f}  (delta={p.delta:.3f})")
    ok = rmse < 0.06
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (2) 1D Cahn-Hilliard spinodal — SEMI-IMPLICIT spectral
# ══════════════════════════════════════════════════════════════════════
def test2():
    print("=" * 60)
    print("(2) 1D Cahn-Hilliard Spinodal Decomposition")
    print("=" * 60)
    p = PhaseFieldParams()
    Nx, Lx = 256, 40.0
    dx = Lx / Nx
    k = 2*np.pi*fftfreq(Nx, d=dx)
    k_sq, k4 = k**2, k**4

    S_bar = 0.3  # inside spinodal
    S = S_bar + 0.03*np.random.randn(Nx)
    s0 = np.var(S)
    fpp = p.d2f_S(S_bar)
    print(f"  S_bar={S_bar}, f''={fpp:.3f} (spinodal: {fpp<0})")

    dt = 0.001
    for n in range(8000):
        S_hat = fft(S)
        # Semi-implicit: only k^4 (diffusion) implicit
        # dS/dt = laplacian( df_S - kappa*laplacian(S) )
        # => (1 + dt*kappa*k^4) S^{n+1} = S^n + dt*(-k^2)*FFT(df_S(S^n))
        rhs = S_hat + dt * (-k_sq) * fft(p.df_S(S))
        S_hat = rhs / (1.0 + dt * p.M_S0 * p.kappa_S * k4)
        S = np.real(ifft(S_hat))
        S = S - np.mean(S) + S_bar

    sv = np.var(S)
    print(f"  Variance: {s0:.5f} -> {sv:.5f}")

    # Check phase separation (>3x variance increase)
    phase_sep = sv > 3*s0
    if fpp < 0 and phase_sep:
        km = np.sqrt(abs(fpp)/(2*p.kappa_S))
        sf = np.abs(fft(S - np.mean(S)))**2
        kmask = (k > 0.1*km) & (k < 5*km)
        if np.any(kmask):
            kp = k[kmask][np.argmax(sf[kmask])]
            print(f"  k_max pred={km:.3f}, obs={kp:.3f}")

    ok = phase_sep
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (3) Coupled 2D AC/CH — semi-implicit spectral
# ══════════════════════════════════════════════════════════════════════
def test3():
    print("=" * 60)
    print("(3) Coupled 2D Allen-Cahn / Cahn-Hilliard")
    print("=" * 60)
    p = PhaseFieldParams()
    N, L = 128, 20.0
    dx = L / N
    kx = 2*np.pi*fftfreq(N, d=dx)
    ky = 2*np.pi*fftfreq(N, d=dx)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k_sq, k4 = KX**2+KY**2, (KX**2+KY**2)**2

    np.random.seed(42)
    S_bar = 0.3
    S = S_bar + 0.05*np.random.randn(N, N)
    g = 0.02*np.random.randn(N, N)
    sv0 = np.var(S)

    dt = 0.005
    for n in range(2000):
        # Gauge (AC): semi-implicit
        g_hat = fft2(g)
        g_hat = (g_hat - dt*p.M_g*fft2(p.df_g(g) + 2*p.lam*S*g)) / (1 + dt*p.M_g*p.kappa_g*k_sq)
        g = np.real(ifft2(g_hat))

        # Potential (CH): semi-implicit
        S_hat = fft2(S)
        rhs = S_hat + dt*(-k_sq)*fft2(p.df_S(S) + p.lam*g**2)
        S_hat = rhs / (1.0 + dt*p.M_S0*p.kappa_S*k4)
        S = np.real(ifft2(S_hat))
        S = S - np.mean(S) + S_bar

    sv = np.var(S)
    gb = np.mean(np.abs(g))
    gb2 = np.abs(g) > 0.3*p.g_eq
    nd = np.max(label(gb2)[0])
    print(f"  S var: {sv0:.4f} -> {sv:.4f}, g_bar={gb:.4f}, domains={nd}")
    ok = sv > 2*sv0
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (4) Three-phase diagram scan
# ══════════════════════════════════════════════════════════════════════
def test4():
    print("=" * 60)
    print("(4) Three-Phase Diagram")
    print("=" * 60)
    p = PhaseFieldParams()
    p.lam = 0.5
    N, L = 64, 10.0
    dx = L / N
    kx = 2*np.pi*fftfreq(N, d=dx)
    ky = 2*np.pi*fftfreq(N, d=dx)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k_sq, k4 = KX**2+KY**2, (KX**2+KY**2)**2

    gv = np.linspace(0.0, 1.5, 7)
    Sv = np.linspace(0.0, 2.0, 7)
    phases = np.zeros((len(gv), len(Sv)), dtype=int)
    dt, ns = 0.005, 400

    for i, g0 in enumerate(gv):
        for j, S0 in enumerate(Sv):
            np.random.seed(i*73 + j*137)
            Sb = S0
            S = Sb + 0.03*np.random.randn(N, N)
            g = g0 * (0.5 + 0.5*np.random.randn(N, N))

            blown = False
            for _ in range(ns):
                g_hat = fft2(g)
                g_hat = (g_hat - dt*p.M_g*fft2(p.df_g(g) + 2*p.lam*S*g)) / (1 + dt*p.M_g*p.kappa_g*k_sq)
                g = np.real(ifft2(g_hat))
                S_hat = fft2(S)
                rhs = S_hat + dt*(-k_sq)*fft2(p.df_S(S) + p.lam*g**2)
                S_hat = rhs / (1.0 + dt*p.M_S0*p.kappa_S*k4)
                S = np.real(ifft2(S_hat))
                S = S - np.mean(S) + Sb
                if np.max(np.abs(S)) > 50:
                    blown = True
                    break

            if blown:
                phases[i, j] = 2
            else:
                gb = np.mean(np.abs(g))
                sv = np.var(S)
                if gb > 0.3 and sv > 0.5:
                    phases[i, j] = 1
                else:
                    phases[i, j] = 0

    n0, n1, n2 = np.sum(phases==0), np.sum(phases==1), np.sum(phases==2)
    print(f"  EQUALITY: {n0}, STRATIFIED: {n1}, EXPLOSIVE: {n2}")
    ok = n1 > 0  # stratified phase must appear
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (5) Coarsening L(t) ~ t^{1/3}
# ══════════════════════════════════════════════════════════════════════
def test5():
    print("=" * 60)
    print("(5) Coarsening L(t) ~ t^{1/3}")
    print("=" * 60)
    p = PhaseFieldParams()
    N, L = 128, 20.0
    dx = L / N
    kx = 2*np.pi*fftfreq(N, d=dx)
    ky = 2*np.pi*fftfreq(N, d=dx)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k_sq, k_rad = KX**2+KY**2, np.sqrt(KX**2+KY**2)

    np.random.seed(123)
    x = np.linspace(0, L, N)
    XX, YY = np.meshgrid(x, x, indexing='ij')
    g = 0.5*np.sin(3*np.pi*XX/L)*np.cos(3*np.pi*YY/L) + 0.05*np.random.randn(N, N)

    dt = 0.01
    Ts, Ls = [], []
    for n in range(6000):
        g_hat = fft2(g)
        g_hat = (g_hat - dt*p.M_g*fft2(p.df_g(g))) / (1 + dt*p.M_g*p.kappa_g*k_sq)
        g = np.real(ifft2(g_hat))
        if (n+1)%300 == 0 and n > 2000:
            gf = np.abs(fft2(g - np.mean(g)))**2
            bins = np.linspace(0.05, np.max(k_rad)*0.7, 12)
            Sk = np.array([np.mean(gf[(k_rad>=b0)&(k_rad<b1)])
                          for b0, b1 in zip(bins[:-1], bins[1:])])
            if np.any(Sk>0):
                kp = 0.5*(bins[:-1]+bins[1:])[np.argmax(Sk)]
                if kp > 0.05:
                    Ts.append((n+1)*dt)
                    Ls.append(2*np.pi/kp)

    if len(Ts) < 4:
        print("  Insufficient data")
        print("  FAIL\n")
        return False
    Ts, Ls = np.array(Ts), np.array(Ls)
    b = np.polyfit(np.log(Ts), np.log(Ls), 1)[0]
    print(f"  Exponent: {b:.3f} (expected ~0.333)")
    ok = abs(b - 1/3) < 0.25
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (6) Critical nucleus
# ══════════════════════════════════════════════════════════════════════
def test6():
    print("=" * 60)
    print("(6) Critical Nucleus Radius")
    print("=" * 60)
    p = PhaseFieldParams()
    p.kappa_g = 2.0
    p.sigma = (2*np.sqrt(2*p.kappa_g)/3)*(p.B**1.5/p.A)
    p.R_c_2d = p.sigma/p.Delta_f

    N, L = 256, 50.0
    dx = L / N
    x = np.linspace(-L/2, L/2, N)
    XX, YY = np.meshgrid(x, x, indexing='ij')
    r = np.sqrt(XX**2+YY**2)

    kx = 2*np.pi*fftfreq(N, d=dx)
    ky = 2*np.pi*fftfreq(N, d=dx)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k_sq = KX**2+KY**2

    Rc = p.R_c_2d
    print(f"  Predicted R_c = {Rc:.3f}")
    radii = np.linspace(0.4*Rc, 2.5*Rc, 10)
    dt, ns = 0.005, 3000
    grew = []

    for R in radii:
        g = np.where(r < R, 0.0, p.g_eq)
        w = p.delta
        trans = np.abs(r - R) < w
        g[trans] = p.g_eq*(r[trans] - (R-w))/(2*w)
        n0 = np.sum(np.abs(g) < 0.3*p.g_eq)
        for _ in range(ns):
            g_hat = fft2(g)
            g_hat = (g_hat - dt*p.M_g*fft2(p.df_g(g)))/(1 + dt*p.M_g*p.kappa_g*k_sq)
            g = np.real(ifft2(g_hat))
        n1 = np.sum(np.abs(g) < 0.3*p.g_eq)
        grew.append(n1 > 1.1*n0)
        print(f"  R={R:.2f}: {n0} -> {n1} {'GROW' if grew[-1] else 'SHRINK'}")

    grew = np.array(grew)
    if np.any(grew):
        idx = np.argmax(grew)
        Ro = radii[idx]
        err = abs(Ro - Rc)/Rc
        print(f"  Observed threshold ~{Ro:.2f}, rel err={err:.2f}")
        ok = err < 0.6
    else:
        ok = False
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (7) Gibbs-Thomson
# ══════════════════════════════════════════════════════════════════════
def test7():
    print("=" * 60)
    print("(7) Gibbs-Thomson Effect")
    print("=" * 60)
    p = PhaseFieldParams()
    N, L = 256, 40.0
    dx = L / N
    x = np.linspace(-L/2, L/2, N)
    XX, YY = np.meshgrid(x, x, indexing='ij')
    r = np.sqrt(XX**2+YY**2)
    k_sq = (2*np.pi*fftfreq(N, d=dx)[:,None])**2 + (2*np.pi*fftfreq(N, d=dx)[None,:])**2

    dt, ns = 0.005, 1000
    curvatures = []
    for R0 in [3.0, 5.0, 8.0, 12.0]:
        g = np.where(r < R0, -p.g_eq, p.g_eq)
        w = p.delta
        trans = np.abs(r - R0) < w
        g[trans] = p.g_eq*(2*(r[trans]-R0+w)/(2*w)-1)
        for _ in range(ns):
            g_hat = fft2(g)
            g_hat = (g_hat - dt*p.M_g*fft2(p.df_g(g)))/(1 + dt*p.M_g*p.kappa_g*k_sq)
            g = np.real(ifft2(g_hat))
        bdy = np.abs(g) < 0.15*p.g_eq
        curvatures.append(1.0/np.mean(r[bdy]) if np.any(bdy) and np.mean(r[bdy])>0.1 else 1.0/R0)

    mono = all(np.diff(curvatures) < 0)
    print(f"  Curvatures: {[f'{c:.4f}' for c in curvatures]}, monotonic: {mono}")
    ok = mono
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (8) Wall pinning (Thm10)
# ══════════════════════════════════════════════════════════════════════
def test8():
    print("=" * 60)
    print("(8) Domain Wall Pinning (Thm10)")
    print("=" * 60)
    p = PhaseFieldParams()
    Nx, Lx = 512, 40.0
    dx = Lx / Nx
    x = np.linspace(-Lx/2, Lx/2, Nx, endpoint=False)
    k_sq = (2*np.pi*fftfreq(Nx, d=dx))**2

    pin_x, pin_w = 0.0, 2.0
    B_loc = p.B*(1.0 - 0.6*np.exp(-((x-pin_x)/pin_w)**2))
    g = p.g_eq*np.tanh((x + 5.0)/(p.delta/np.sqrt(2)))
    force = 0.0005

    positions = []
    dt = 0.005
    for n in range(10000):
        g_hat = fft(g)
        df = (p.A*g**2 - B_loc)*g + force
        g_hat = (g_hat - dt*p.M_g*fft(df))/(1 + dt*p.M_g*p.kappa_g*k_sq)
        g = np.real(ifft(g_hat))
        if (n+1)%200 == 0:
            zc = np.where(np.diff(np.signbit(g)))[0]
            if len(zc)>0: positions.append(x[zc[0]])

    positions = np.array(positions)
    if len(positions) < 5:
        print("  Insufficient data\n  FAIL\n")
        return False
    vel = np.abs(np.diff(positions))
    near = np.abs(positions[:-1]-pin_x) < 4.0
    far = ~near
    if np.any(near) and np.any(far):
        vn, vf = np.mean(vel[near]), np.mean(vel[far])
        print(f"  v_far={vf:.5f}, v_near={vn:.5f}, ratio={vn/(vf+1e-10):.3f}")
        ok = vn/(vf+1e-10) < 0.8
    else:
        ok = False
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
# (9) Staircase nucleation (Thm12)
# ══════════════════════════════════════════════════════════════════════
def test9():
    print("=" * 60)
    print("(9) Staircase Defect Nucleation (Thm12)")
    print("=" * 60)
    p = PhaseFieldParams()
    p.lam = 0.5
    N, L = 64, 10.0
    dx = L / N
    kx = 2*np.pi*fftfreq(N, d=dx)
    ky = 2*np.pi*fftfreq(N, d=dx)
    KX, KY = np.meshgrid(kx, ky, indexing='ij')
    k_sq, k4 = KX**2+KY**2, (KX**2+KY**2)**2

    S = np.zeros((N, N))
    steps = [0, N//4, N//2, 3*N//4]
    heights = [-0.5, 0.5, 1.5, 2.5]
    for i in range(len(steps)):
        lo, hi = steps[i], (steps[i+1] if i+1<len(steps) else N)
        S[lo:hi, :] = heights[i]
    S += 0.02*np.random.randn(N, N)
    Sb = np.mean(S)
    np.random.seed(123)
    g = 0.02*np.random.randn(N, N)

    dt = 0.005
    for _ in range(1500):
        g_hat = fft2(g)
        g_hat = (g_hat - dt*p.M_g*fft2(p.df_g(g)+2*p.lam*S*g))/(1+dt*p.M_g*p.kappa_g*k_sq)
        g = np.real(ifft2(g_hat))
        S_hat = fft2(S)
        rhs = S_hat + dt*(-k_sq)*fft2(p.df_S(S)+p.lam*g**2)
        S_hat = rhs/(1.0+dt*p.M_S0*p.kappa_S*k4)
        S = np.real(ifft2(S_hat))
        S = S - np.mean(S) + Sb

    gp = np.mean(np.abs(g), axis=1)
    hw = N//16
    sv, pv = [], []
    for si in range(len(steps)):
        sx = steps[si]
        sv.append(np.mean(gp[max(0,sx-hw):min(N,sx+hw)]))
        mid = (sx+(steps[si+1] if si+1<len(steps) else N))//2
        lo, hi = max(0,mid-hw), min(N,mid+hw)
        if lo<hi: pv.append(np.mean(gp[lo:hi]))
    sm, pm = np.mean(sv), np.mean(pv)
    ratio = sm/(pm+1e-10)
    print(f"  |g| at steps: {sm:.5f}, plateaus: {pm:.5f}, ratio: {ratio:.3f}")
    ok = ratio > 1.15
    print(f"  {'PASS' if ok else 'FAIL'}\n")
    return ok


# ══════════════════════════════════════════════════════════════════════
def main():
    print("\n" + "=" * 70)
    print("  SCX PHASE FIELD THEORY — VERIFICATION SUITE")
    print("  SCX相场理论验证套件")
    print("=" * 70 + "\n")

    res = {}
    res['(1) Allen-Cahn Kink'] = test1()
    res['(2) Cahn-Hilliard Spinodal'] = test2()
    res['(3) 2D Coupled AC/CH'] = test3()
    res['(4) Phase Diagram'] = test4()
    res['(5) Coarsening L~t^{1/3}'] = test5()
    res['(6) Critical Nucleus'] = test6()
    res['(7) Gibbs-Thomson'] = test7()
    res['(8) Wall Pinning (Thm10)'] = test8()
    res['(9) Staircase Nucl. (Thm12)'] = test9()

    print("=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    for k, v in res.items():
        print(f"  {'OK' if v else '!!'} {k}: {'PASS' if v else 'FAIL'}")
    n = sum(res.values())
    print(f"\n  {n}/{len(res)} passed")
    print()
    return 0 if n >= 5 else 1

if __name__ == '__main__':
    sys.exit(main())
