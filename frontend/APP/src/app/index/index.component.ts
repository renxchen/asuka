import { Component, OnInit, ElementRef, AfterViewInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { IndexService } from './index.service';
import { BreadCrumbComponent } from '../../components/breadCrumb/bread-crumb';
import { TweenLite } from 'gsap';
declare var $: any;
@Component({
    selector: 'index',
    templateUrl: 'index.html',
    styleUrls: ['./index.less']
})

export class IndexComponent implements OnInit, AfterViewInit {
    private minWidthFlg: boolean;
    @ViewChild(BreadCrumbComponent) breadCrumb: BreadCrumbComponent;
    constructor(
        private elementRef: ElementRef,
        private service: IndexService,
        private activatedRoute: ActivatedRoute
    ) {}
    ngOnInit() {
        localStorage.setItem('requestFailed', '');
    }
    ngAfterViewInit() {
        let _t  = this;
        $('#side-menu').metisMenu();
        $('.close-canvas-menu').click(function () {
            $('body').toggleClass('mini-navbar');
            _t.SmoothlyMenu();
        });
        let contnet = this. elementRef.nativeElement.querySelector('div.wrapper-content');
        TweenLite.from(contnet, 1.5, { opacity: 0, top: -20 } );
    }
    public toggleClass() {
        $('body').toggleClass('mini-navbar');
        this.SmoothlyMenu();
    }
    public SmoothlyMenu() {
        if (!$('body').hasClass('mini-navbar') || $('body').hasClass('body-small')) {
            $('#side-menu').show();
            setTimeout(
                function () {
                    $('#side-menu').fadeIn(400);
                }, 200);
        } else if ($('body').hasClass('fixed-sidebar')) {
            $('#side-menu').hide();
            setTimeout(
                function () {
                    $('#side-menu').fadeIn(0);
                }, 100);
        } else {
            $('#side-menu').removeAttr('style');
        }
    }
    public logout() {
        this.service.logout().subscribe(res => {});
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('sessionTimeOut');
      }
}
