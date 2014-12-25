#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# arxiv - arxiv plugin for calibre
# Copyright 2012 Abdó Roig-Maranges <abdo.roig@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# NOTE:
#
# This file encodes tag assignations to arxiv topics and AMS mathematical subject
# classification keys.
#
# This is tuned to my particular interests, and may not be suitable for others.


import re



_arxiv_tags ={

    # Cosmology and Astrophysics                                          #
    # ------------------------------------------------------------------- #

    'astro-ph.CO':          ['physics', 'cosmology'],
    'astro-ph.EP':          ['physics', 'astrophysics'],
    'astro-ph.GA':          ['physics', 'astrophysics'],
    'astro-ph.HE':          ['physics', 'astrophysics'],
    'astro-ph.IM':          ['physics', 'astrophysics', 'experimental'],
    'astro-ph.SR':          ['physics', 'astrophysics'],



    # Condensed matter                                                    #
    # ------------------------------------------------------------------- #

    'cond-mat.dis-nn':      ['physics', 'condensed matter'],
    'cond-mat.mtrl-sci':    ['physics', 'condensed matter'],
    'cond-mat.mes-hall':    ['physics', 'condensed matter'],
    'cond-mat.other':       ['physics', 'condensed matter'],
    'cond-mat.quant-gas':   ['physics', 'condensed matter'],
    'cond-mat.soft':        ['physics', 'condensed matter'],
    'cond-mat.stat-mech':   ['physics', 'statistical mechanics'],
    'cond-mat.str-el':      ['physics', 'condensed matter'],
    'cond-mat.supr-con':    ['physics', 'condensed matter', 'superconductors'],



    # Gravity                                                             #
    # ------------------------------------------------------------------- #

    'gr-qc':                ['physics', 'general relativity'],



    # Quantum mechanics                                                   #
    # ------------------------------------------------------------------- #

    'quant-ph':             ['physics', 'quantum mechanics'],



    # Particle physics                                                    #
    # ------------------------------------------------------------------- #

    'hep-ex':               ['physics', 'experimental', 'particle physics'],
    'hep-lat':              ['physics', 'experimental', 'particle physics', 'lattice'],
    'hep-ph':               ['physics', 'phenomenology', 'particle physics'],
    'hep-th':               ['physics', 'qft', 'particle physics'],
    'math-ph':              ['physics'],
    'nucl-ex':              ['physics', 'experimental', 'nuclear physics'],
    'nucl-th':              ['physics', 'nuclear physics'],



    # Experimental physics                                                #
    # ------------------------------------------------------------------- #

    'physics.acc-ph':       ['physics', 'experimental', 'particle physics', 'particle accelerators'],
    'physics.ao-ph':        ['physics', 'atmospheric physics'],
    'physics.atom-ph':      ['physics', 'atomic physics'],
    'physics.atm-clus':     ['physics', 'atomic physics'],
    'physics.bio-ph':       ['physics', 'biological physics'],
    'physics.chem-ph':      ['physics', 'chemical physics'],
    'physics.class-ph':     ['physics', 'classical mechanics'],
    'physics.comp-ph':      ['physics', 'computational physics'],
    'physics.data-an':      ['physics', 'statistics'],
    'physics.flu-dyn':      ['physics', 'fluid dynamics'],
    'physics.gen-ph':       ['physics'],
    'physics.geo-ph':       ['physics', 'geophysics'],
    'physics.hist-ph':      ['physics', 'history'],
    'physics.ins-det':      ['physics', 'instrumentation', 'experimental'],
    'physics.med-ph':       ['physics', 'medical physics'],
    'physics.optics':       ['physics', 'optics'],
    'physics.ed-ph':        ['physics', 'education'],
    'physics.soc-ph':       ['physics', 'sociology'],
    'physics.plasm-ph':     ['physics', 'plasma'],
    'physics.pop-ph':       ['physics', 'divulgation'],
    'physics.space-ph':     ['physics'],



    # Mathematics                                                         #
    # ------------------------------------------------------------------- #

    'math.AG':              ['maths', 'algebraic geometry'],
    'math.AT':              ['maths', 'algebraic topology'],
    'math.AP':              ['maths', 'analysis', 'pde'],
    'math.CT':              ['maths', 'category theory'],
    'math.CA':              ['maths', 'analysis'],
    'math.CO':              ['maths', 'combinatorics'],
    'math.AC':              ['maths', 'algebra', 'commutative algebra'],
    'math.CV':              ['maths', 'analysis', 'complex analysis'],
    'math.DG':              ['maths', 'differential geometry'],
    'math.DS':              ['maths', 'analysis', 'dynamical systems'],
    'math.FA':              ['maths', 'functional analysis'],
    'math.GM':              ['maths'],
    'math.GN':              ['maths', 'topology'],
    'math.GT':              ['maths', 'geometric topology'],
    'math.GR':              ['maths', 'group theory'],
    'math.HO':              ['maths', 'history'],
    'math.IT':              ['maths', 'information theory'],
    'math.KT':              ['maths', 'K-theory'],
    'math.LO':              ['maths', 'logic'],
    'math.MP':              ['maths', 'physics'],
    'math.MG':              ['maths', 'metric geometry'],
    'math.NT':              ['maths', 'number theory'],
    'math.NA':              ['maths', 'numerical methods'],
    'math.OA':              ['maths', 'operator algebras', 'functional analysis'],
    'math.OC':              ['maths', 'optimization'],
    'math.PR':              ['maths', 'probability'],
    'math.QA':              ['maths', 'algebra', 'quantum'],
    'math.RT':              ['maths', 'algebra', 'representation theory'],
    'math.RA':              ['maths', 'algebra', 'associative algebra'],
    'math.SP':              ['maths', 'functional analysis'],
    'math.ST':              ['maths', 'statistics'],
    'math.SG':              ['maths', 'differential geometry', 'symplectic geometry']

    # TODO: Nonlinear Sciences
    # TODO: Computer Science
    # TODO: Quantitative Biology
    # TODO: Quantitative Finance
    # TODO: Statistics
}



_msc_tags = {
    '03':                  ['maths', 'logic'],
    '05':                  ['maths', 'combinatorics'],
    '06':                  ['maths', 'algebra'],
    '08':                  ['maths', 'algebra'],
    '11':                  ['maths', 'number theory'],
    '13':                  ['maths', 'commutative algebra'],

    # Algebraic Geometry                                                  #
    # ------------------------------------------------------------------- #

    '14':                  ['maths', 'algebraic geometry'],
    '14A22':               ['noncommutative'],

    '14B05':               ['singularities'],
    '14B07':               ['deformation theory'],
    '14B12':               ['deformation theory'],
    '14B15':               ['local cohomology'],
    '14B20':               ['formal geometry'],

    '14C05':               ['moduli'],
    '14C15':               ['equivariant'],
    '14C17':               ['algebraic cycles', 'intersection theory'],
    '14C25':               ['algebraic cycles'],
    '14C30':               ['algebraic cycles', 'hodge theory'],
    '14C35':               ['K-theory', 'algebraic cycles'],
    '14C40':               ['riemann-roch'],

    '14D07':               ['hodge theory'],
    '14D10':               ['arithmetic geometry'],
    '14D15':               ['deformation theory'],
    '14D20':               ['moduli'],
    '14D21':               ['moduli', 'physics'],
    '14D22':               ['moduli'],
    '14D23':               ['stacks'],
    '14D24':               ['geometric langlands'],

    '14E':                 [' birational geometry'],
    '14E15':               ['resolution of singularities'],
    '14E16':               ['mckay correspondence'],
    '14E18':               ['motivic integration'],
    '14E30':               ['minimal model program'],

    '14F05':               ['derived category', 'coherent sheaves'],
    '14F10':               ['D-modules'],
    '14F17':               ['cohomology', 'vanishing theorems'],
    '14F18':               ['multiplier ideals'],
    '14F20':               ['grothendieck topologies'],
    '14F22':               ['brauer group'],
    '14F25':               ['cohomology'],
    '14F30':               ['p-adic'],
    '14F35':               ['homotopy theory'],
    '14F40':               ['de rham', 'cohomology'],
    '14F42':               ['motivic homotopy'],
    '14F43':               ['cohomology'],

    '14G':                 ['arithmetic geometry'],
    '14G10':               ['zeta functions'],
    '14G17':               ['characteristic p'],
    '14G22':               ['rigid analytic geometry'],
    '14G35':               ['shimura varieties'],
    '14G40':               ['arakelov geometry'],
    '14G50':               ['cryptography'],

    '14H':                 ['algebraic curves'],
    '14H10':               ['moduli'],
    '14H15':               ['moduli'],
    '14H52':               ['elliptic curves'],
    '14H60':               ['vector bundles'],
    '14H70':               ['integrable systems'],
    '14H81':               ['physics'],

    '14J':                 ['algebraic surfaces'],
    '14J10':               ['moduli'],
    '14J15':               ['moduli'],
    '14J17':               ['singularities'],
    '14J32':               ['calabi-yau'],
    '14J33':               ['mirror symmetry'],
    '14J45':               ['fano varieties'],
    '14J60':               ['vector bundles'],
    '14J80':               ['topology'],
    '14J81':               ['physics'],

    '14K':                 ['abelian varieties'],
    '14K10':               ['moduli'],
    '14K22':               ['complex multiplication'],

    '14L':                 ['algebraic groups'],

    '14M15':               ['flag varieties'],
    '14M20':               ['rational varieties'],
    '14M22':               ['rationally connected'],
    '14M25':               ['toric varieties'],
    '14M30':               ['supergeometry'],

    '14N35':               ['gromov-witten'],
    '14P':                 ['real algebraic geometry'],
    '14Q':                 ['computer science'],
    '14T':                 ['tropical geometry'],



    # Noncommutative algebra                                              #
    # ------------------------------------------------------------------- #

    # Linear algebra
    '15A':                 ['linear algebra'],

    # Noncommutative algebras
    '16':                  ['maths', 'algebra', 'noncommutative'],
    '16G':                 ['representation theory'],
    '16T05':               ['hopf algebras'],
    '16T10':               ['bialgebras'],
    '16T25':               ['yang-baxter'],
    '16T30':               ['combinatorics'],

    '16W55':               ['superalgebra'],
    '16Z':                 ['computer science'],

    # Nonassociative algebras
    '17':                  ['maths', 'algebra', 'nonassociative'],

    '17B':                 ['lie algebras'],
    '17B35':               ['quantum groups', 'quantum'],
    '17B55':               ['homological algebra'],
    '17B56':               ['cohomology'],
    '17B67':               ['kac-moody', 'infinite dimensional'],
    '17B68':               ['virasoro algebra'],
    '17B69':               ['vertex algebras'],
    '17B80':               ['integrable systems'],
    '17B81':               ['physics'],

    '17C':                 ['jordan algebras'],
    '17C65':               ['infinite dimensional'],
    '17C70':               ['superalgebra'],
    '17C90':               ['physics'],

    # categories and homological algebra
    '18':                  ['maths'],

    '18A':                 ['category theory'],

    '18B':                 ['category theory'],

    '18C':                 ['category theory'],

    '18D':                 ['category theory'],
    '18D20':               ['enriched categories'],
    '18D50':               ['operads'],

    '18E':                 ['abelian categories', 'category theory'],

    '18F':                 ['category theory'],
    '18F10':               ['grothendieck topologies'],

    '18G':                 ['homological algebra'],
    '18G25':               ['relative homological algebra'],
    '18G30':               ['simplicial'],
    '18G40':               ['spectral sequences'],
    '18G50':               ['nonabelian cohomology'],
    '18G55':               ['model categories'],


    # K-theory
    '19':                  ['maths', 'K-theory'],

    '19D':                 ['homotopy theory'],

    '19E':                 ['algebraic geometry'],
    '19E15':               ['algebraic cycles'],

    '19F':                 ['number theory'],

    '19K':                 ['operator algebras'],

    # Groups
    '20':                  ['maths', 'groups'],

    '20C':                 ['representation theory'],

    # Lie groups
    '20C':                 ['topological groups'],
    '20D':                 ['topological groups'],
    '22E':                 ['lie groups'],



    # Analysis                                                            #
    # ------------------------------------------------------------------- #

    # real analysis
    '26':                  ['maths', 'analysis', 'real analysis'],

    # measure theory
    '28':                  ['maths', 'analysis', 'measure theory'],

    # complex analysis
    '30':                  ['maths', 'analysis', 'complex analysis'],

    # several complex variables
    '32':                  ['maths'],
    '32A':                 ['complex analysis', 'analysis'],

    '32C':                 ['differential geometry'],
    '32C15':               ['complex geometry'],
    '32C38':               ['D-modules'],

    '32D':                 ['complex analysis', 'analysis'],
    '32E':                 ['complex analysis', 'analysis'],

    '32G':                 ['differential geometry', 'complex geometry', 'deformation theory'],
    '32H':                 ['differential geometry', 'complex geometry'],
    '32J':                 ['differential geometry', 'complex geometry'],

    '32Q':                 ['differential geometry', 'complex geometry'],
    '32Q15':               ['kahler geometry'],
    '32Q20':               ['kahler-einstein'],
    '32Q25':               ['calabi-yau'],
    '32Q28':               ['stein manifolds'],
    '32Q65':               ['J-holomorphic curves'],

    '32S':                 ['singularities', 'complex geometry'],
    '32S30':               ['deformation theory'],
    '32S35':               ['hodge theory'],
    '32S40':               ['monodromy'],

    '32V':                 ['CR geometry'],

    '32W':                 ['differential operators'],
    '32W20':               ['monge-ampere'],
    '32W30':               ['heat flow'],

    '34':                  ['maths', 'analysis', 'ode'],

    '35':                  ['maths', 'analysis', 'pde'],

    '37':                  ['maths', 'dynamical systems'],

    '40':                  ['maths', 'analysis'],

    '41':                  ['maths', 'analysis'],

    '42':                  ['maths', 'analysis', 'fourier analysis'],

    '43':                  ['maths', 'analysis', 'harmonic analysis'],

    '44':                  ['maths', 'analysis'],

    '45':                  ['maths', 'analysis'],

    '46':                  ['maths', 'analysis', 'functional analysis'],

    '47':                  ['maths', 'analysis', 'operator algebras'],

    '49':                  ['maths', 'analysis', 'variational calculus'],



    # Geometry and Topology                                               #
    # ------------------------------------------------------------------- #

    '51':                  ['maths', 'geometry'],

    '52':                  ['maths', 'discrete geometry'],

    '53':                  ['maths', 'differential geometry'],

    # Differential geometry
    '53B05':               ['connections'],
    '53B10':               ['connections'],
    '53B15':               ['connections'],
    '53B20':               ['riemannian geometry'],
    '53B21':               ['riemannian geometry'],
    '53B30':               ['pseudo-riemannian geometry'],
    '53B35':               ['kahler geometry', 'complex geometry'],
    '53B40':               ['finsler geometry'],
    '53B50':               ['physics'],

    '53C05':               ['connections'],
    '53C07':               ['connections'],
    '53C08':               ['gerbes'],
    '53C12':               ['foliations'],
    '53C20':               ['riemannian geometry'],
    '53C21':               ['riemannian geometry', 'pde'],
    '53C26':               ['hyper-kahler', 'complex geometry'],
    '53C28':               ['twistors'],
    '53C35':               ['symmetric spaces'],
    '53C43':               ['harmonic maps', 'geometric analysis'],
    '53C44':               ['geometric flows', 'geometric analysis'],
    '53C50':               ['pseudo-riemannian geometry'],
    '53C55':               ['kahler geometry', 'complex geometry'],
    '53C56':               ['complex geometry'],
    '53C60':               ['finsler geometry'],
    '53C65':               ['integral geometry'],
    '53C80':               ['physics'],

    '53D':                 ['symplectic geometry'],
    '53D10':               ['contact geometry'],
    '53D15':               ['contact geometry'],
    '53D17':               ['poisson geometry'],
    '53D18':               ['generalized geometries'],
    '53D25':               ['geometric flows'],
    '53D30':               ['moduli'],
    '53D37':               ['mirror symmetry'],
    '53D40':               ['floer homology'],
    '53D45':               ['gromov-witten'],
    '53D50':               ['geometric quantization', 'quantization'],
    '53D55':               ['deformation quantization', 'quantization'],

    '53Z':                 ['physics'],

    # Topology
    '54':                  ['maths', 'topology'],

    # Algebrac topology
    '55':                  ['maths', 'topology'],
    '55N05':               ['cech cohomology'],
    '55N10':               ['homology'],
    '55N15':               ['K-theory'],
    '55N20':               ['stable homotopy', 'homotopy theory'],
    '55N30':               ['sheaves', 'cohomology'],
    '55N33':               ['intersection homology'],
    '55N91':               ['equivariant'],

    '55P':                 ['homotopy theory'],
    '55P35':               ['loop spaces'],
    '55P42':               ['stable homotopy'],
    '55P45':               ['operads'],
    '55P50':               ['string topology'],
    '55P62':               ['rational homotopy'],
    '55P91':               ['equivariant'],

    '55Q':                 ['homotopy theory'],

    '55R':                 ['bundles'],
    '55S':                 ['cohomology operations'],
    '55T':                 ['spectral sequences'],

    # Manifolds
    '57':                  ['maths', 'topology'],
    '57N20':               ['infinite dimensional'],
    '57Q':                 ['PL topology'],
    '57R':                 ['differential topology', 'manifolds'],

    # Global geometry and analysis
    '58':                  ['maths', 'differential geometry'],
    '58A12':               ['de rham'],
    '58A14':               ['hodge theory'],
    '58A20':               ['jets'],
    '58A50':               ['supergeometry'],
    '58B':                 ['infinite dimensional'],
    '58B32':               ['quantum groups', 'quantum'],
    '58B34':               ['noncommutative'],
    '58C40':               ['spectral geometry'],
    '58C50':               ['supergeometry'],
    '58D':                 ['moduli'],
    '58E':                 ['infinite dimensional', 'geometric analysis'],
    '58E30':               ['variational calculus'],
    '58E20':               ['harmonic maps', 'geometric analysis'],
    '58J':                 ['geometric analysis'],
    '58J28':               ['chern-simons'],
    '58K':                 ['catastrophe theory'],
    '58Z':                 ['physics'],



    # Probability and statistics                                          #
    # ------------------------------------------------------------------- #

    '60':                  ['maths', 'probability'],

    '62':                  ['maths', 'statistics'],

    '65':                  ['maths', 'numerical methods'],



    # Computer science                                                    #
    # ------------------------------------------------------------------- #

    '68':                  ['computer science'],



    # Physics                                                             #
    # ------------------------------------------------------------------- #

    '70':                  ['classical mechanics'],

    '76':                  ['fluid mechanics'],

    '78':                  ['physics', 'optics'],

    '80':                  ['physics', 'thermodynamics'],

    # quantum theory
    '81':                  ['physics', 'quantum'],

    '81P40':               ['entanglement'],
    '81P45':               ['information theory'],
    '81P68':               ['computer science'],
    '81P70':               ['computer science', 'coding theory'],
    '81P94':               ['computer science', 'cryptography'],

    '81Q60':               ['susy'],

    '81R':                 ['lie groups'],
    '81R60':               ['noncommutative'],

    '81S':                 ['quantum mechanics'],
    '81S10':               ['geometric quantization'],
    '81S40':               ['path integral'],

    '81T':                 ['qft'],
    '81T13':               ['gauge theory'],
    '81T15':               ['perturbative', 'renormalization'],
    '81T16':               ['nonperturbative', 'renormalization'],
    '81T17':               ['renormalization'],
    '81T30':               ['string theory'],
    '81T60':               ['susy'],
    '81T75':               ['noncommutative', 'differential geometry'],

    '81U':                 ['scattering theory'],

    '81V05':               ['qcd', 'particle physics'],
    '81V10':               ['qed', 'particle physics'],
    '81V15':               ['electroweak theory', 'particle physics'],
    '81V17':               ['quantum gravity'],
    '81V25':               ['particle physics'],
    '81V35':               ['nuclear physics'],
    '81V45':               ['atomic physics'],
    '81V55':               ['molecular physics'],
    '81V80':               ['quantum optics'],

    '82':                  ['physics', 'statistical mechanics'],

    '83':                  ['physics'],

    '83A':                 ['special relativity'],

    '83C':                 ['general relativity'],
    '83C22':               ['classical electrodynamics'],
    '83C57':               ['black holes'],
    '83C60':               ['twistors'],
    '83C65':               ['noncommutative', 'differential geometry'],
    '83C75':               ['black holes'],

    '83E15':               ['kaluza-klein'],
    '83E30':               ['string theory'],
    '83E50':               ['supergravity', 'susy'],

    '83F':                 ['cosmology'],



    # Applications                                                        #
    # ------------------------------------------------------------------- #

    '90':                  ['maths', 'optimization'],
}




# Interface                                                           #
# ------------------------------------------------------------------- #


def arxiv_tags(subj):
    return _arxiv_tags.get(subj, [])


def msc_tags(subj):

    tags = set()
    m = re.match('([0-9]+)([A-Z]+)([0-9]+)', subj)

    if m:
        level1 = '%02d'   % int(m.group(1))
        level2 = '%s%s'   % (level1, m.group(2))
        level3 = '%s%02d' % (level2, int(m.group(3)))

        tags.update(_msc_tags.get(level1, []))
        tags.update(_msc_tags.get(level2, []))
        tags.update(_msc_tags.get(level3, []))

    return tags
